# Network & Streaming Reference

## Table of Contents
- [WiFi Connection](#wifi-connection)
- [HTTP Client](#http-client)
- [HTTP Server & Streaming](#http-server--streaming)
- [WebSocket](#websocket)
- [MQTT](#mqtt)
- [TCP Socket](#tcp-socket)
- [RTSP/RTMP Streaming](#rtsp-rtmp-streaming)

## WiFi Connection

### Connect to WiFi
```python
from maix import network, err

def connect_wifi(ssid, password):
    w = network.wifi.Wifi()
    e = w.connect(ssid, password, wait=True, timeout=60)
    err.check_raise(e, "connect wifi failed")
    print("Connected! IP:", w.get_ip())
    return w

w = connect_wifi("YourSSID", "YourPassword")
```

### WiFi AP Mode (Hotspot)
```python
from maix import network

w = network.wifi.Wifi()
w.start_ap("MaixPyAP", "12345678", channel=6)
print("AP started, IP:", w.get_ip())
```

### Get WiFi Info
```python
w = network.wifi.Wifi()
print("IP:", w.get_ip())
print("SSID:", w.ssid())
print("MAC:", w.mac())
print("RSSI:", w.rssi())
```

## HTTP Client

### GET Request
```python
from maix import http

response = http.get("http://httpbin.org/get")
print("Status:", response.status_code)
print("Body:", response.text)
```

### POST Request
```python
from maix import http
import json

data = {"name": "MaixPy", "version": "v4"}
response = http.post(
    "http://httpbin.org/post",
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
)
print("Response:", response.text)
```

### Download File
```python
response = http.get("http://example.com/file.zip")
with open("file.zip", "wb") as f:
    f.write(response.content)
```

## HTTP Server & Streaming

### JPEG Stream Server
```python
from maix import camera, display, app, http, time

html = """<!DOCTYPE html>
<html>
<head><title>MaixPy Stream</title></head>
<body>
    <h1>MaixPy Camera Stream</h1>
    <img src="/stream" alt="Stream">
</body>
</html>"""

cam = camera.Camera(320, 240)
stream = http.JpegStreamer()
stream.set_html(html)
stream.start()

print(f"Stream URL: http://{stream.host()}:{stream.port()}")

while not app.need_exit():
    img = cam.read()
    stream.write(img)
```

### Custom HTTP Server
```python
from maix import http, app

server = http.Server()

@server.route("/", "GET")
def index(request):
    return http.Response("<h1>Hello MaixPy!</h1>")

@server.route("/api/data", "GET")
def get_data(request):
    return http.Response('{"status": "ok"}', content_type="application/json")

server.start(port=8080)
print(f"Server: http://{server.host()}:{server.port()}")

while not app.need_exit():
    server.poll()
    time.sleep_ms(10)
```

## WebSocket

### WebSocket Client
```python
from maix import websocket, app, time

client = websocket.Client()
client.connect("ws://echo.websocket.org")

def on_message(msg):
    print("Received:", msg)

client.on_message(on_message)

while not app.need_exit():
    client.send("Hello!")
    client.poll()
    time.sleep_ms(100)
```

### WebSocket Server
```python
from maix import websocket, app, time

server = websocket.Server(port=8765)

def on_connect(client):
    print("Client connected")

def on_message(client, msg):
    print("Message:", msg)
    client.send("Echo: " + msg)

server.on_connect(on_connect)
server.on_message(on_message)
server.start()

while not app.need_exit():
    server.poll()
    time.sleep_ms(10)
```

## MQTT

### MQTT Publish/Subscribe
```python
from maix import mqtt, app, time

client = mqtt.Client("maixpy_client")

# Connect to broker
client.connect("broker.hivemq.com", 1883)

# Subscribe to topic
def on_message(topic, payload):
    print(f"Topic: {topic}, Message: {payload}")

client.subscribe("maixpy/test")
client.on_message(on_message)

# Main loop
counter = 0
while not app.need_exit():
    # Publish message
    client.publish("maixpy/test", f"Hello {counter}")
    counter += 1

    # Process incoming messages
    client.loop(timeout_ms=100)
    time.sleep_ms(1000)
```

### MQTT with QoS
```python
# Publish with QoS
client.publish("maixpy/data", "important", qos=1)

# Subscribe with QoS
client.subscribe("maixpy/cmd", qos=1)
```

## TCP Socket

### TCP Client
```python
from maix import socket

client = socket.Socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.100", 8080))

# Send data
client.send(b"Hello Server")

# Receive data
data = client.recv(1024)
print("Received:", data)

client.close()
```

### TCP Server
```python
from maix import socket, app, time

server = socket.Socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))
server.listen(5)

print("Server listening on port 8080")

while not app.need_exit():
    # Accept connection (non-blocking check)
    try:
        client, addr = server.accept()
        print(f"Connection from {addr}")

        data = client.recv(1024)
        if data:
            client.send(b"Echo: " + data)
        client.close()
    except:
        pass

    time.sleep_ms(100)
```

## RTSP/RTMP Streaming

### RTSP Server
```python
from maix import camera, rtsp, app

cam = camera.Camera(640, 480)
server = rtsp.Server(port=8554)
server.start()

print(f"RTSP URL: rtsp://{server.host()}:{server.port()}/stream")

while not app.need_exit():
    img = cam.read()
    server.write(img)
```

### RTMP Streaming
```python
from maix import camera, rtmp, app

cam = camera.Camera(640, 480)

# Stream to RTMP server (e.g., YouTube, Twitch)
stream = rtmp.Stream("rtmp://your-server/live/stream_key")
stream.start()

while not app.need_exit():
    img = cam.read()
    stream.write(img)
```

## USB Video (UVC)

### USB Camera Mode
```python
from maix import camera, uvc, app

cam = camera.Camera(640, 480)
uvc_dev = uvc.UVC()
uvc_dev.start()

while not app.need_exit():
    img = cam.read()
    uvc_dev.write(img)
```

## Get Local IP

```python
from maix import network
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

print("Local IP:", get_local_ip())
```

## Network Utilities

```python
from maix import network

# Check if connected
w = network.wifi.Wifi()
if w.is_connected():
    print("WiFi connected")

# Scan networks
networks = w.scan()
for n in networks:
    print(f"SSID: {n['ssid']}, RSSI: {n['rssi']}, Encrypted: {n['encrypted']}")
```
