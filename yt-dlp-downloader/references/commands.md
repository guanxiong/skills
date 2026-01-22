# yt-dlp Common Commands Reference

This file contains quick reference for common yt-dlp commands and options.

## Basic Commands

### Download video
```bash
yt-dlp <URL>
```

### Download to specific directory
```bash
yt-dlp -o "path/to/downloads/%(title)s.%(ext)s" <URL>
```

### Download best quality
```bash
yt-dlp -f "bestvideo+bestaudio/best" <URL>
```

### Download audio only
```bash
yt-dlp -x --audio-format mp3 <URL>
```

## Format Selection

### Best quality (merges video and audio)
```
bestvideo+bestaudio/best
```

### Best MP4
```
bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best
```

### Specific resolution (1080p or lower)
```
bestvideo[height<=1080]+bestaudio/best
```

### Specific resolution (720p or lower)
```
bestvideo[height<=720]+bestaudio/best
```

### Audio only (best quality)
```
bestaudio/best
```

### Audio only (MP3)
```
bestaudio[ext=m4a]/bestaudio/best
```

## Subtitle Options

### Download available subtitles
```bash
yt-dlp --write-subs <URL>
```

### Download auto-generated subtitles
```bash
yt-dlp --write-auto-subs <URL>
```

### Download specific language
```bash
yt-dlp --write-subs --sub-langs en,zh <URL>
```

### Convert subtitles to SRT
```bash
yt-dlp --write-subs --convert-subs srt <URL>
```

## Metadata Options

### Download description
```bash
yt-dlp --write-description <URL>
```

### Download metadata as JSON
```bash
yt-dlp --write-info-json <URL>
```

### Download thumbnail
```bash
yt-dlp --write-thumbnail <URL>
```

### Download all metadata
```bash
yt-dlp --write-description --write-info-json --write-thumbnail <URL>
```

## Playlist Options

### Download entire playlist
```bash
yt-dlp <PLAYLIST_URL>
```

### Download playlist items 5-10
```bash
yt-dlp --playlist-start 5 --playlist-end 10 <PLAYLIST_URL>
```

### Download single video from playlist
```bash
yt-dlp --no-playlists <PLAYLIST_URL>
```

### List playlist items without downloading
```bash
yt-dlp --dump-single-json --flat-playlist <PLAYLIST_URL>
```

## Information Gathering

### Get video info (JSON)
```bash
yt-dlp --dump-json <URL>
```

### Get video title
```bash
yt-dlp --get-title <URL>
```

### Get video duration
```bash
yt-dlp --get-duration <URL>
```

### Get video description
```bash
yt-dlp --get-description <URL>
```

### List available formats
```bash
yt-dlp --list-formats <URL>
```

### List available subtitles
```bash
yt-dlp --list-subs <URL>
```

## Output Templates

### Default
```
%(title)s.%(ext)s
```

### With uploader
```
%(uploader)s - %(title)s.%(ext)s
```

### With date
```
%(upload_date)s - %(title)s.%(ext)s
```

### Organized by channel
```
%(uploader)s/%(title)s.%(ext)s
```

### With playlist info
```
%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s
```

### All available fields
```
Available fields:
- id, title, fulltitle, uploader, uploader_id, uploader_url
- channel, channel_id, channel_url
- duration, view_count, like_count, dislike_count
- upload_date, release_date
- description, categories, tags
- playlist_index, playlist_title, playlist_id
- width, height, fps, codec, ext, filesize, filesize_approx
- format, format_id, format_note
- epoch, autonumber
```

## Advanced Options

### Rate limit
```bash
yt-dlp --limit-rate 1M <URL>
```

### Retry on failure
```bash
yt-dlp --retries 5 <URL>
```

### Continue incomplete downloads
```bash
yt-dlp --continue <URL>
```

### Proxy support
```bash
yt-dlp --proxy http://proxy.example.com:8080 <URL>
```

### User agent
```bash
yt-dlp --user-agent "Mozilla/5.0..." <URL>
```

### Extractor arguments (site-specific)
```bash
# YouTube: use cookies for age-restricted videos
yt-dlp --cookies cookies.txt <URL>

# Twitch: use authentication
yt-dlp --username user --password pass <URL>
```

## Common Issues & Solutions

### Age-restricted videos
```bash
# Option 1: Use cookies
yt-dlp --cookies cookies.txt <URL>

# Option 2: Use browser cookies
yt-dlp --cookies-from-browser chrome <URL>
```

### Region-restricted videos
```bash
yt-dlp --proxy <COUNTRY_PROXY> <URL>
```

### Private videos
```bash
yt-dlp --username <EMAIL> --password <PASSWORD> <URL>
```

### Slow downloads
```bash
# Use lower quality
yt-dlp -f "bestvideo[height<=720]+bestaudio/best" <URL>

# Use aria2 for multi-threaded download
yt-dlp --external-downloader aria2c <URL>
```

### Download fails
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Increase retries
yt-dlp --retries 10 <URL>

# Use verbose mode to debug
yt-dlp --verbose <URL>
```

## Format ID Examples

| Format ID | Description |
|-----------|-------------|
| `bestvideo+bestaudio/best` | Best quality (merges video + audio) |
| `best` | Best pre-merged format (no merging needed) |
| `bestvideo[height<=1080]+bestaudio/best` | Best quality up to 1080p |
| `worst` | Worst quality |
| `bestaudio` | Best audio only |
| `bestvideo` | Best video only (no audio) |

## Supported Sites (Partial List)

- **YouTube**: youtube.com, youtu.be
- **Vimeo**: vimeo.com
- **Twitch**: twitch.tv, clips.twitch.tv
- **Twitter/X**: twitter.com, x.com
- **Facebook**: facebook.com, fb.watch
- **Instagram**: instagram.com
- **TikTok**: tiktok.com
- **Reddit**: reddit.com, v.redd.it
- **Bilibili**: bilibili.com
- **Dailymotion**: dailymotion.com
- **SoundCloud**: soundcloud.com
- **Bandcamp**: bandcamp.com
- **Vimeo**: vimeo.com
- **And 1000+ more...**

For complete list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
