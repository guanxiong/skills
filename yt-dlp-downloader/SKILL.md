---
name: yt-dlp-downloader
description: "Download videos from YouTube and 1000+ other websites using yt-dlp. Use when you need to download videos, extract audio, download subtitles, download playlists, get video info, select quality, or download metadata."
---

# yt-dlp Video Downloader

Use yt-dlp (youtube-dl fork) to download videos from YouTube and 1000+ other websites.

## Installation

Install yt-dlp:

```bash
pip install yt-dlp
```

For additional features (like downloading M3U8/HLS native formats):

```bash
pip install yt-dlp[default,curl]
```

Or download the standalone executable:

```bash
# Windows
winget install yt-dlp

# macOS
brew install yt-dlp

# Linux
sudo apt install yt-dlp  # or your package manager
```

## Quick Start

### Proxy (Automatic Detection)

**IMPORTANT**: By default, this skill automatically detects and uses proxy from multiple sources with priority:

**Priority**:
1. Chrome browser proxy (system settings)
2. Clash proxy (ports 7890-7899)

This helps with:

- Accessing geo-restricted content
- Bypassing network restrictions
- Better connectivity in restricted environments

**How it works**: The skill checks Chrome proxy settings first, then scans for Clash proxy on ports 7890-7899.

**For non-mainland services (e.g., YouTube)**:
- The skill automatically tests if the service is accessible
- If direct access fails, it searches for available proxies
- Proxies are tested before use
- Detailed proxy information is displayed

**Note**: If no proxy is found in Chrome or Clash, no proxy will be used.

### Browser Cookies (Default Behavior)

**IMPORTANT**: By default, this skill uses Chrome browser cookies to download videos, especially for YouTube. This helps with:

- Accessing age-restricted videos
- Bypassing geo-restrictions
- Downloading private videos
- Better success rate in general

**Requirements**: You must have Chrome installed and logged in to the video platform.

```python
# Default: uses Chrome cookies
result = download_video("https://youtube.com/watch?v=VIDEO_ID")

# Explicitly specify browser
result = download_video(
    "https://youtube.com/watch?v=VIDEO_ID",
    cookies_browser="chrome"  # or "firefox", "edge", "safari"
)
```

**Supported browsers**: chrome, firefox, edge, safari, opera, brave, vivaldi, chromium

### Basic Download

```python
from scripts.download_video import download_video

# Basic download (uses Chrome cookies by default)
result = download_video("https://youtube.com/watch?v=VIDEO_ID")

# Download to specific directory
result = download_video(
    "https://youtube.com/watch?v=VIDEO_ID",
    output_dir="./downloads"
)

# Download with subtitles
result = download_video(
    "https://youtube.com/watch?v=VIDEO_ID",
    write_subs=True,
    write_auto_subs=True,
    sub_lang="en"
)
```

### File Already Exists

**Important**: When downloading, the skill checks if the video file already exists in the output directory. If found:

- **Information is displayed** showing existing file(s) and their sizes
- **yt-dlp skips re-download** to avoid duplicates
- **This is normal behavior** - it prevents file overwrite

**To re-download a file**:

1. Delete the existing file manually, then try again
2. Download to a different directory
3. Use a different output filename (not currently supported)

**Example output when file exists**:
```
[Checking for existing files...]
[INFO] Found 1 existing file(s) for this video:
  - My Video.f401.mp4 (100.50 MB)
[INFO] yt-dlp will skip re-download if file already exists.
[INFO] This is normal behavior to avoid duplicates.

[INFO] To re-download:
  1. Delete existing file, then try again
  2. Download to a different directory
  3. Specify a different output filename
```

### Disable Browser Cookies

If you don't want to use browser cookies:

```python
# Disable cookies by setting to None or empty string
result = download_video(
    "https://youtube.com/watch?v=VIDEO_ID",
    cookies_browser=""  # or cookies_browser=None
)
```

**Note**: Disabling cookies may reduce success rate, especially for age-restricted or geo-restricted videos.

### Manual Proxy Configuration

If you want to specify a custom proxy instead of using auto-detected proxies (Chrome or Clash):

```python
# Use specific proxy
result = download_video(
    "https://youtube.com/watch?v=VIDEO_ID",
    proxy="http://proxy-server:port"
)

# Use SOCKS5 proxy
result = download_video(
    "https://youtube.com/watch?v=VIDEO_ID",
    proxy="socks5://proxy-server:port"
)
```

**Proxy priority**:
1. Manual proxy (if specified with `proxy` parameter)
2. Chrome proxy settings (automatic)
3. No proxy (if Chrome has no proxy configured)

**Note**: Manual proxy overrides Chrome proxy settings.

## Getting Video Information

Before downloading, get video information:

```python
from scripts.download_video import get_video_info

info = get_video_info("https://youtube.com/watch?v=VIDEO_ID")
if info["success"]:
    video_data = info["info"]
    print(f"Title: {video_data.get('title')}")
    print(f"Duration: {video_data.get('duration')} seconds")
    print(f"Description: {video_data.get('description')[:200]}...")
```

## Listing Available Formats

To see all available formats:

```python
from scripts.download_video import list_formats

formats = list_formats("https://youtube.com/watch?v=VIDEO_ID")
if formats["success"]:
    print(formats["formats"])
```

## Download Options

### Format Selection

Control quality and format:

```python
# Best quality (video + audio)
download_video(url, format_id="bestvideo+bestaudio/best")

# Best MP4 video
download_video(url, format_id="bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best")

# 1080p or lower
download_video(url, format_id="bestvideo[height<=1080]+bestaudio/best")

# Audio only
download_video(url, format_id="bestaudio/best")
```

Common format options:

- `bestvideo+bestaudio/best` - Best quality (merges video and audio)
- `bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best` - Best MP4
- `bestvideo[height<=720]+bestaudio/best` - Max 720p
- `bestaudio/best` - Audio only

### Subtitles

Download subtitles:

```python
download_video(url,
    write_subs=True,        # Download available subtitles
    write_auto_subs=True,   # Download auto-generated subtitles
    sub_lang="en,zh"        # Specify languages
)
```

### Additional Metadata

```python
download_video(url,
    write_description=True,   # Download description
    write_info_json=True,      # Download metadata JSON
    write_thumbnail=True       # Download thumbnail
)
```

### Playlist Options

Download entire playlist or part of it:

```python
# Download entire playlist
download_video(playlist_url)

# Download specific items from playlist (e.g., items 5-10)
download_video(playlist_url,
    playlist_start=5,
    playlist_end=10
)

# Download single video from playlist
download_video(playlist_url,
    no_playlists=True
)

# Download playlist as flat list (no actual download)
download_video(playlist_url,
    extract_flat=True
)
```

## Supported Sites

yt-dlp supports 1000+ websites including:

- YouTube (videos, playlists, channels)
- Vimeo
- Dailymotion
- Twitch
- Twitter/X
- Facebook
- Instagram
- TikTok
- Reddit
- Bilibili
- And many more...

Check the full list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## Error Handling

```python
result = download_video(url)

if result["success"]:
    print(f"Success! Downloaded to: {result['output_dir']}")
else:
    print(f"Error: {result['error']}")
    if "stderr" in result:
        print(f"Details: {result['stderr']}")
```

Common errors:

- **yt-dlp not installed**: Run `pip install yt-dlp`
- **Video unavailable**: Video might be private, deleted, or region-locked
- **Age restricted**: The skill uses browser cookies by default. Ensure Chrome is installed and logged in.
- **Cookies not found**: If you see "unable to get cookies", try:
  - Make sure Chrome is installed and running
  - Make sure you're logged into the video platform in Chrome
  - Try a different browser: `cookies_browser="firefox"`
  - Disable cookies: `cookies_browser=""`
- **Proxy issues**: If you see proxy-related errors:
  - Check if Chrome is configured to use a proxy
  - Check if Clash is running (skill auto-detects Clash on ports 7890-7899)
  - Try manually specifying a proxy: `proxy="http://proxy:port"`
  - Disable proxy by not configuring one in Chrome or stopping Clash
- **Network blocked (YouTube)**: If YouTube downloads fail with SSL/TLS errors:
  - The skill automatically detects and uses proxy from Chrome or Clash
  - Configure a proxy in Chrome settings or start Clash if needed
  - Or manually specify: `proxy="http://proxy:port"`

## Advanced Usage

### Browser Cookies (Default Authentication)

The skill automatically uses Chrome cookies for authentication:

```python
# Default behavior - uses Chrome cookies
result = download_video(url)

# Specify different browser
result = download_video(url, cookies_browser="firefox")

# Disable cookies
result = download_video(url, cookies_browser="")
```

### Manual Cookies (for private/age-restricted videos)

For age-restricted or private videos, you can also use manual cookies:

```bash
# Export cookies from browser (using browser extension)
# Then use them with yt-dlp
yt-dlp --cookies cookies.txt <URL>
```

### Custom Output Template

Control output filename:

```python
# The script uses: %(title)s.%(ext)s
# For more control, use yt-dlp directly via subprocess:
import subprocess
subprocess.run([
    "yt-dlp",
    "-o", "%(uploader)s/%(title)s.%(ext)s",
    url
])
```

See yt-dlp documentation for all output template options:
https://github.com/yt-dlp/yt-dlp#output-template

### Proxy Support

Download through proxy:

```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'http://proxy.example.com:8080'
download_video(url)
```

## Best Practices

1. **Check video info first**: Use `get_video_info()` before downloading to verify the video is available
2. **Use appropriate quality**: Lower quality for faster downloads, higher quality for archival
3. **Handle errors gracefully**: Always check the `result["success"]` field
4. **Respect rate limits**: Don't download too many videos too quickly
5. **Batch downloads**: For multiple videos, download one at a time with small delays

## Examples

### Example 1: Download YouTube video

```python
from scripts.download_video import download_video

result = download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(result)
```

### Example 2: Download with subtitles

```python
result = download_video(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    write_subs=True,
    write_auto_subs=True
)
```

### Example 3: Download playlist items 1-5

```python
result = download_video(
    "https://www.youtube.com/playlist?list=PLAYLIST_ID",
    playlist_start=1,
    playlist_end=5
)
```

### Example 4: Get video info without downloading

```python
from scripts.download_video import get_video_info

info = get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
if info["success"]:
    print(f"Title: {info['info']['title']}")
    print(f"Duration: {info['info']['duration']} seconds")
```

## Troubleshooting

### Video not downloading

1. Check if video URL is accessible in browser
2. Update yt-dlp: `pip install --upgrade yt-dlp`
3. Try different format selection
4. Check error message for specific issues

### Slow download speed

1. Try different format (lower quality)
2. Check network connection
3. Consider downloading during off-peak hours

### Subtitles not downloading

1. Check if subtitles are available: `get_video_info()`
2. Try different subtitle languages
3. Auto-generated subtitles may not be available

## Resources

- yt-dlp GitHub: https://github.com/yt-dlp/yt-dlp
- yt-dlp Documentation: https://github.com/yt-dlp/yt-dlp#readme
- Format selection: https://github.com/yt-dlp/yt-dlp#format-selection
- Supported sites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
