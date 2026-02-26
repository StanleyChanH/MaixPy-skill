# LLM & VLM Reference (MaixCAM2 Only)

**Note**: LLM/VLM features are only available on MaixCAM2 (1GB/4GB memory). MaixCAM and MaixCAM-Pro do not support these features.

## Table of Contents
- [Qwen LLM](#qwen-llm)
- [DeepSeek LLM](#deepseek-llm)
- [VLM (Vision Language Model)](#vlm-vision-language-model)
- [Memory Management](#memory-management)
- [Performance Tips](#performance-tips)

## Qwen LLM

### Basic Usage
```python
from maix import nn, err, log, sys

# Set log level to reduce noise
log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

# Check memory before loading model
def show_mem():
    print("Memory:")
    for k, v in sys.memory_info().items():
        print(f"  {k}: {sys.bytes_to_human(v)}")

show_mem()

# Load Qwen model
# Options: Qwen2.5-0.5B-Instruct or Qwen2.5-1.5B-Instruct
model = "/root/models/Qwen2.5-0.5B-Instruct/model.mud"
qwen = nn.Qwen(model)

show_mem()

# Simple chat
response = qwen.send("Hello, please introduce yourself")
err.check_raise(response.err_code)
print("Response:", response.msg)
```

### With Callback (Streaming)
```python
from maix import nn, err, log

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")

def on_reply(obj, resp):
    """Called for each token/chunk"""
    print(resp.msg_new, end="", flush=True)

qwen.set_reply_callback(on_reply)

# Now responses will stream
msg = "Tell me a short story"
print(">>", msg)
resp = qwen.send(msg)
err.check_raise(resp.err_code)
print()  # New line after streaming
```

### System Prompt
```python
qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")

# Set system prompt to customize behavior
qwen.set_system_prompt(
    "You are a helpful assistant for embedded systems development. "
    "Keep responses concise and practical."
)

response = qwen.send("How do I use GPIO?")
print(response.msg)
```

### Context Management
```python
qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")

# First message
qwen.send("My name is Alice")

# Second message - remembers context
resp = qwen.send("What's my name?")
print(resp.msg)  # Should mention Alice

# Clear context to start fresh
qwen.clear_context()

# Now it won't remember previous conversation
resp = qwen.send("What's my name?")
print(resp.msg)  # Won't know the name
```

### Multi-turn Conversation
```python
from maix import nn, err, log, app, time

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)
qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")

history = []

def chat(user_input):
    """Send message and maintain history"""
    resp = qwen.send(user_input)
    err.check_raise(resp.err_code)

    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": resp.msg})

    return resp.msg

# Conversation loop
print("Chat with Qwen (type 'quit' to exit)")
while not app.need_exit():
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    response = chat(user_input)
    print(f"Qwen: {response}")
```

## DeepSeek LLM

DeepSeek models work similarly to Qwen:

```python
from maix import nn, err, log

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

# Load DeepSeek model
model = "/root/models/DeepSeek-R1-Distill-Qwen-1.5B/model.mud"
deepseek = nn.DeepSeek(model)

# Same API as Qwen
response = deepseek.send("Explain quantum computing in simple terms")
err.check_raise(response.err_code)
print(response.msg)
```

## VLM (Vision Language Model)

### InternVL (Image Understanding)
```python
from maix import nn, camera, display, image, err, log, app

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

# Load VLM model
vlm = nn.VLM(model="/root/models/InternVL2-1B/model.mud")

# Initialize camera
cam = camera.Camera(640, 480)
disp = display.Display()

while not app.need_exit():
    img = cam.read()

    # Ask question about the image
    question = "What objects do you see in this image?"
    response = vlm.ask(img, question)

    err.check_raise(response.err_code)
    print(f"Q: {question}")
    print(f"A: {response.msg}")

    # Display image with response
    img.draw_string(10, 10, response.msg[:50], image.COLOR_RED)
    disp.show(img)

    time.sleep_ms(100)
```

### VLM with Callback
```python
from maix import nn, camera, image, log

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

vlm = nn.VLM("/root/models/InternVL2-1B/model.mud")

def on_response(obj, resp):
    print(resp.msg_new, end="", flush=True)

vlm.set_reply_callback(on_response)

# Capture image
cam = camera.Camera(640, 480)
img = cam.read()

# Ask with streaming response
vlm.ask(img, "Describe this image in detail")
```

### VLM Use Cases

```python
from maix import nn, camera, image, log

vlm = nn.VLM("/root/models/InternVL2-1B/model.mud")
cam = camera.Camera(640, 480)

# Object detection via natural language
img = cam.read()
response = vlm.ask(img, "Count the number of people in this image")
print(f"People count: {response.msg}")

# OCR
response = vlm.ask(img, "Read all the text visible in this image")
print(f"Text: {response.msg}")

# Scene understanding
response = vlm.ask(img, "What room is this? What activities can be done here?")
print(f"Scene: {response.msg}")

# Safety check
response = vlm.ask(img, "Are there any safety hazards in this image?")
print(f"Safety: {response.msg}")
```

## Memory Management

### Check Memory
```python
from maix import sys

def show_memory():
    info = sys.memory_info()
    print("Memory Info:")
    print(f"  Total: {sys.bytes_to_human(info['total'])}")
    print(f"  Used: {sys.bytes_to_human(info['used'])}")
    print(f"  Free: {sys.bytes_to_human(info['free'])}")
    print(f"  Available: {sys.bytes_to_human(info['available'])}")

show_memory()
```

### Memory Considerations

| Model | Size | Min RAM Required | Recommended Device |
|-------|------|------------------|-------------------|
| Qwen2.5-0.5B | ~500MB | 1GB | MaixCAM2 (1GB+) |
| Qwen2.5-1.5B | ~1.5GB | 2GB | MaixCAM2 (4GB) |
| InternVL2-1B | ~1GB | 2GB | MaixCAM2 (4GB) |

### Free Memory After Use
```python
# LLM models use significant memory
# Delete instance when done to free memory

qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")
# ... use the model ...

# Free memory
del qwen

import gc
gc.collect()
```

## Performance Tips

### Model Selection

1. **Qwen2.5-0.5B**: Faster (~9 tokens/s), less accurate
2. **Qwen2.5-1.5B**: Slower (~4 tokens/s), more accurate

### Optimization

```python
from maix import nn, log, sys

# Reduce log output for better performance
log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

# Use smaller model for faster response
qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")

# Keep prompts concise for faster processing
response = qwen.send("Summarize in one sentence: ...")
```

### Benchmark Results (MaixCAM2)

| Model | First Token Latency | Tokens/Second |
|-------|---------------------|---------------|
| Qwen2.5-0.5B | ~640ms | ~9 tokens/s |
| Qwen2.5-1.5B | ~1610ms | ~4 tokens/s |

## Model Download

Models should be placed in `/root/models/`:

```bash
# Download from HuggingFace or MaixHub
# Example structure:
/root/models/
├── Qwen2.5-0.5B-Instruct/
│   └── model.mud
├── Qwen2.5-1.5B-Instruct/
│   └── model.mud
└── InternVL2-1B/
    └── model.mud
```

Download links:
- Qwen2.5-0.5B: https://huggingface.co/sipeed/Qwen2.5-0.5B-Instruct-maixcam2
- Qwen2.5-1.5B: https://huggingface.co/sipeed/Qwen2.5-1.5B-Instruct-maixcam2
- InternVL2-1B: Available via MaixHub

## Error Handling

```python
from maix import nn, err, log

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

try:
    qwen = nn.Qwen("/root/models/Qwen2.5-0.5B-Instruct/model.mud")
    response = qwen.send("Hello")

    if response.err_code != err.Err.ERR_NONE:
        print(f"Error: {response.err_code}")
    else:
        print(response.msg)

except Exception as e:
    print(f"Failed to load model: {e}")
    # Model may not exist or not enough memory
```

## Integration Example: Smart Camera

```python
from maix import nn, camera, display, image, app, time, log, sys

log.set_log_level(log.LogLevel.LEVEL_ERROR, color=False)

# Check device supports VLM
if sys.device_id() != "maixcam2":
    print("VLM requires MaixCAM2")
    exit(1)

# Initialize
vlm = nn.VLM("/root/models/InternVL2-1B/model.mud")
cam = camera.Camera(640, 480)
disp = display.Display()

last_analysis = time.ticks_ms()

while not app.need_exit():
    img = cam.read()

    # Analyze scene every 5 seconds
    if time.ticks_ms() - last_analysis > 5000:
        response = vlm.ask(img, "Describe what you see briefly")
        analysis = response.msg[:100]  # Truncate for display
        last_analysis = time.ticks_ms()

    # Display
    if 'analysis' in locals():
        img.draw_string(10, 10, analysis, image.COLOR_WHITE, scale=1.5)
    disp.show(img)
```
