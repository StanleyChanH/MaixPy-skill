# Audio Reference

## Table of Contents
- [Audio Playback](#audio-playback)
- [Audio Recording](#audio-recording)
- [Volume Control](#volume-control)
- [Text-to-Speech (TTS)](#text-to-speech-tts)
- [Speech Recognition (ASR)](#speech-recognition-asr)

## Audio Playback

### Blocking Playback
```python
from maix import audio

# Play WAV file (blocks until complete)
player = audio.Player("/root/test.wav")
print(f"Sample Rate: {player.sample_rate()}")
print(f"Format: {player.format()}")
print(f"Channels: {player.channel()}")

player.volume(80)  # Set volume 0-100
player.play()

print("Playback complete!")
```

### Non-Blocking Playback
```python
from maix import audio, app, time

player = audio.Player("/root/test.wav")
player.volume(80)

# Start playback (non-blocking)
player.play_nonblock()

# Do other work while playing
while not app.need_exit():
    if not player.is_playing():
        print("Playback finished")
        break
    # Do other tasks here
    time.sleep_ms(10)

player.stop()
```

### Play from Bytes
```python
from maix import audio

# Read audio file into memory
with open("/root/test.wav", "rb") as f:
    audio_data = f.read()

player = audio.Player(audio_data)
player.play()
```

### Supported Formats
- WAV (PCM, ADPCM)
- MP3
- AAC
- OGG

## Audio Recording

### Blocking Recording
```python
from maix import audio

# Record 5 seconds of audio
recorder = audio.Recorder("/root/recording.wav", sample_rate=16000, channels=1)
recorder.record(duration=5000)  # Duration in milliseconds

print("Recording saved to /root/recording.wav")
```

### Non-Blocking Recording
```python
from maix import audio, app, time

recorder = audio.Recorder("/root/recording.wav", sample_rate=16000)
recorder.record_nonblock()

print("Recording started...")

start_time = time.ticks_ms()
while not app.need_exit():
    if time.ticks_ms() - start_time > 5000:  # Record for 5 seconds
        recorder.stop()
        print("Recording stopped")
        break
    time.sleep_ms(100)
```

### Record with Callback
```python
from maix import audio

def on_audio_data(data):
    # Process audio chunk in real-time
    print(f"Received {len(data)} bytes")
    # Could send to ASR, process, etc.

recorder = audio.Recorder(callback=on_audio_data, sample_rate=16000)
recorder.start()

# Recording continues until stop()
# time.sleep(10)
# recorder.stop()
```

## Volume Control

### Set Volume
```python
from maix import audio

player = audio.Player("/root/test.wav")

# Set volume (0-100)
player.volume(50)  # 50% volume

# Get current volume
vol = player.volume()
print(f"Current volume: {vol}")
```

### System Volume
```python
from maix import audio

# Set system-wide volume
audio.set_volume(80)

# Get system volume
vol = audio.get_volume()
print(f"System volume: {vol}")
```

## Text-to-Speech (TTS)

### MelloTTS (Offline TTS)
```python
from maix import tts, audio, app

# Initialize TTS engine
tts_engine = tts.MelloTTS()

# Generate speech
text = "Hello, welcome to MaixPy development."
audio_data = tts_engine.synthesize(text)

# Save to file or play
with open("/root/speech.wav", "wb") as f:
    f.write(audio_data)

# Or play directly
player = audio.Player(audio_data)
player.play()
```

### TTS with Different Voices
```python
from maix import tts

tts_engine = tts.MelloTTS()

# List available voices
voices = tts_engine.list_voices()
for v in voices:
    print(f"Voice: {v['name']}, ID: {v['id']}")

# Set voice
tts_engine.set_voice("en-US")
audio_data = tts_engine.synthesize("Hello world")
```

### Chinese TTS
```python
from maix import tts

tts_engine = tts.MelloTTS()
tts_engine.set_voice("zh-CN")

text = "你好，欢迎使用MaixPy开发"
audio_data = tts_engine.synthesize(text)

player = audio.Player(audio_data)
player.play()
```

## Speech Recognition (ASR)

### Offline ASR
```python
from maix import asr, audio, app, time

# Initialize ASR engine
asr_engine = asr.ASR(model="/root/models/asr_model.mud")

# Record and recognize
recorder = audio.Recorder(sample_rate=16000, channels=1)

def on_audio(data):
    result = asr_engine.recognize(data)
    if result:
        print(f"Recognized: {result.text}")

recorder.set_callback(on_audio)
recorder.start()

while not app.need_exit():
    time.sleep_ms(100)
```

### Real-time ASR
```python
from maix import asr, audio, app, time

asr_engine = asr.ASR(model="/root/models/asr_model.mud")

# Continuous recognition
asr_engine.start_continuous()

def on_result(result):
    print(f"Heard: {result.text}")
    if "hello" in result.text.lower():
        print("Hello detected!")

asr_engine.on_result(on_result)

while not app.need_exit():
    time.sleep_ms(100)

asr_engine.stop_continuous()
```

### Whisper ASR
```python
from maix import asr

# Whisper model (more accurate, slower)
whisper = asr.Whisper(model="/root/models/whisper_tiny.mud")

# Transcribe audio file
result = whisper.transcribe("/root/recording.wav")
print(f"Transcription: {result.text}")

# Get segments with timestamps
for seg in result.segments:
    print(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}")
```

## Audio Utilities

### Get Audio Info
```python
from maix import audio

info = audio.get_info("/root/test.wav")
print(f"Duration: {info.duration}ms")
print(f"Sample Rate: {info.sample_rate}")
print(f"Channels: {info.channels}")
print(f"Format: {info.format}")
```

### Convert Format
```python
from maix import audio

# Convert audio format
audio.convert("/root/test.wav", "/root/test.mp3", format="mp3", bitrate="128k")
```

### Audio Device List
```python
from maix import audio

# List playback devices
playback_devices = audio.list_playback_devices()
for dev in playback_devices:
    print(f"Playback: {dev['name']}")

# List recording devices
record_devices = audio.list_record_devices()
for dev in record_devices:
    print(f"Recording: {dev['name']}")
```

## Integration Example: Voice Assistant

```python
from maix import audio, asr, tts, app, time, nn, camera, display

# Initialize components
asr_engine = asr.ASR(model="/root/models/asr_model.mud")
tts_engine = tts.MelloTTS()
player = audio.Player()

def speak(text):
    """Convert text to speech and play"""
    audio_data = tts_engine.synthesize(text)
    player = audio.Player(audio_data)
    player.play()

def listen():
    """Listen and return recognized text"""
    recorder = audio.Recorder(sample_rate=16000, duration=3000)
    audio_data = recorder.record()
    result = asr_engine.recognize(audio_data)
    return result.text if result else ""

# Main loop
speak("Hello, how can I help you?")

while not app.need_exit():
    text = listen()
    if text:
        print(f"Heard: {text}")
        if "hello" in text.lower():
            speak("Hello there!")
        elif "time" in text.lower():
            current_time = time.strftime("%H:%M")
            speak(f"The time is {current_time}")
        elif "exit" in text.lower():
            speak("Goodbye!")
            break
```
