# Peripherals Reference

## Table of Contents
- [GPIO](#gpio)
- [UART](#uart)
- [I2C](#i2c)
- [SPI](#spi)
- [PWM](#pwm)
- [ADC](#adc)
- [Pinmap](#pinmap)

## GPIO

### LED Control
```python
from maix import gpio, pinmap, time, sys, err

# Get pin based on device
device_id = sys.device_id()
if device_id == "maixcam2":
    pin_name = "A6"
    gpio_id = "GPIOA6"
else:
    pin_name = "A14"
    gpio_id = "GPIOA14"

# Set pin function
err.check_raise(pinmap.set_pin_function(pin_name, gpio_id), "set pin failed")

# Control LED
led = gpio.GPIO(gpio_id, gpio.Mode.OUT)
led.value(0)  # Turn off

while True:
    led.toggle()
    time.sleep_ms(500)
```

### GPIO Input
```python
from maix import gpio, pinmap, time, sys, err

device_id = sys.device_id()
if device_id == "maixcam2":
    pin_name = "A7"
    gpio_id = "GPIOA7"
else:
    pin_name = "A13"
    gpio_id = "GPIOA13"

err.check_raise(pinmap.set_pin_function(pin_name, gpio_id), "set pin failed")

btn = gpio.GPIO(gpio_id, gpio.Mode.IN)
while True:
    if btn.value() == 0:  # Button pressed (active low)
        print("Button pressed")
    time.sleep_ms(10)
```

## UART

### Basic UART Communication
```python
from maix import app, uart, pinmap, time, sys, err

device_id = sys.device_id()
if device_id == "maixcam2":
    pin_function = {
        "A21": "UART4_TX",
        "A22": "UART4_RX"
    }
    device = "/dev/ttyS4"
else:
    pin_function = {
        "A16": "UART0_TX",
        "A17": "UART0_RX"
    }
    device = "/dev/ttyS0"

for pin, func in pin_function.items():
    err.check_raise(pinmap.set_pin_function(pin, func), f"Failed set pin{pin}")

serial = uart.UART(device, 115200)

# Send data
serial.write_str("hello world\r\n")

# Read data (non-blocking)
while not app.need_exit():
    data = serial.read()
    if data:
        print("Received:", data)
        serial.write(data)  # Echo back
    time.sleep_ms(1)
```

### UART with Timeout
```python
# Read with timeout (blocking)
data = serial.read(timeout=2000)  # 2 second timeout
if data:
    print("Received:", data)
```

### UART with Callback
```python
from maix import uart, pinmap, sys, err

def on_receive(data):
    print("Callback received:", data)

serial = uart.UART(device, 115200)
serial.set_receive_callback(on_receive)

# Main loop does other work
while True:
    time.sleep_ms(100)
```

### List Available UART Devices
```python
ports = uart.list_devices()
print("Available UART ports:", ports)
```

## I2C

### I2C Master
```python
from maix import i2c, pinmap, sys, err

device_id = sys.device_id()
if device_id == "maixcam2":
    scl_pin = "A1"
    sda_pin = "A0"
    i2c_id = 6
else:
    scl_pin = "A15"
    sda_pin = "A27"
    i2c_id = 5

err.check_raise(pinmap.set_pin_function(scl_pin, f"I2C{i2c_id}_SCL"), "set SCL failed")
err.check_raise(pinmap.set_pin_function(sda_pin, f"I2C{i2c_id}_SDA"), "set SDA failed")

bus = i2c.I2C(i2c_id, i2c.Mode.MASTER)

# Scan for devices
slaves = bus.scan()
print("Found devices:")
for addr in slaves:
    print(f"  0x{addr:02x}")

# Write to device
bus.writeto(0x50, bytes([0x00, 0x01, 0x02]))  # Write 3 bytes to addr 0x50

# Read from device
data = bus.readfrom(0x50, 4)  # Read 4 bytes from addr 0x50

# Write register then read
bus.writeto_mem(0x50, 0x00, bytes([0x01]))  # Write 0x01 to reg 0x00
data = bus.readfrom_mem(0x50, 0x00, 4)  # Read 4 bytes from reg 0x00
```

## SPI

### SPI Master
```python
from maix import spi, pinmap, sys, err

device_id = sys.device_id()
if device_id == "maixcam2":
    cs_pin = "A8"
    sclk_pin = "A9"
    mosi_pin = "A10"
    miso_pin = "A11"
    spi_id = 1
else:
    cs_pin = "A28"
    sclk_pin = "A29"
    mosi_pin = "A30"
    miso_pin = "A31"
    spi_id = 1

# Set pin functions
err.check_raise(pinmap.set_pin_function(cs_pin, f"SPI{spi_id}_CS"), "set CS failed")
err.check_raise(pinmap.set_pin_function(sclk_pin, f"SPI{spi_id}_SCLK"), "set SCLK failed")
err.check_raise(pinmap.set_pin_function(mosi_pin, f"SPI{spi_id}_MOSI"), "set MOSI failed")
err.check_raise(pinmap.set_pin_function(miso_pin, f"SPI{spi_id}_MISO"), "set MISO failed")

# Initialize SPI
dev = spi.SPI(spi_id, spi.Mode.MASTER)

# Write and read
tx_data = bytes([0x01, 0x02, 0x03])
rx_data = dev.write_read(tx_data, len(tx_data))
print("Received:", rx_data)
```

### SPI Loopback Test
```python
# Connect MOSI to MISO for testing
dev = spi.SPI(spi_id, spi.Mode.MASTER)
tx = bytes([0xAA, 0x55, 0x00, 0xFF])
rx = dev.write_read(tx, len(tx))
print("TX:", tx.hex())
print("RX:", rx.hex())
```

## PWM

### PWM LED (Brightness Control)
```python
from maix import pwm, pinmap, time, sys, err

device_id = sys.device_id()
if device_id == "maixcam2":
    pin_name = "A5"
    pwm_name = "PWM5"
else:
    pin_name = "A14"
    pwm_name = "PWM14"

err.check_raise(pinmap.set_pin_function(pin_name, pwm_name), "set pin failed")

# Initialize PWM: channel 0, frequency 1000Hz, duty cycle 50%
p = pwm.PWM(0, 1000, 0.5)
p.enable(True)

# Fade in/out
while True:
    for duty in range(0, 100):
        p.duty(duty / 100.0)
        time.sleep_ms(10)
    for duty in range(100, 0, -1):
        p.duty(duty / 100.0)
        time.sleep_ms(10)
```

### PWM Servo Control
```python
from maix import pwm, pinmap, time

# Servo typically uses 50Hz
servo = pwm.PWM(0, 50, 0.075)  # 7.5% duty = center position
servo.enable(True)

def set_angle(angle):
    """Set servo angle (0-180 degrees)"""
    # 2.5% = 0°, 7.5% = 90°, 12.5% = 180°
    duty = 0.025 + (angle / 180.0) * 0.1
    servo.duty(duty)

while True:
    set_angle(0)
    time.sleep(1)
    set_angle(90)
    time.sleep(1)
    set_angle(180)
    time.sleep(1)
```

## ADC

### ADC Read
```python
from maix import adc, pinmap, time, sys, err

device_id = sys.device_id()
if device_id == "maixcam2":
    pin_name = "A4"
    adc_name = "ADC4"
else:
    pin_name = "A18"
    adc_name = "ADC0"

err.check_raise(pinmap.set_pin_function(pin_name, adc_name), "set pin failed")

# Initialize ADC
a = adc.ADC(0)

while True:
    value = a.read()
    voltage = value * 3.3 / 4095  # Assuming 12-bit ADC, 3.3V reference
    print(f"Raw: {value}, Voltage: {voltage:.2f}V")
    time.sleep_ms(100)
```

## Pinmap

### Get Pin Info
```python
from maix import pinmap, sys

# Get all available pin functions
info = pinmap.get_pin_info()
for pin, funcs in info.items():
    print(f"{pin}: {funcs}")
```

### Device-Specific Pinmap
```python
from maix import sys

device_id = sys.device_id()  # "maixcam", "maixcam2"

# Always check device_id for portable code
if device_id == "maixcam2":
    # MaixCAM2 pin assignments
    uart_tx = "A21"
    uart_rx = "A22"
else:
    # MaixCAM/MaixCAM-Pro pin assignments
    uart_tx = "A16"
    uart_rx = "A17"
```

## Error Handling

```python
from maix import err

# Check and raise error
ret = pinmap.set_pin_function("A14", "GPIOA14")
err.check_raise(ret, "Failed to set pin function")

# Or check manually
if ret != err.Err.ERR_NONE:
    print(f"Error: {ret}")
```
