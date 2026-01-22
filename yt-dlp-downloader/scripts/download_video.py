#!/usr/bin/env python3
"""
yt-dlp video downloader script
Supports downloading videos with customizable options
"""
import subprocess
import sys
import json
import os
import platform
import socket
import urllib.request
import urllib.error
from pathlib import Path

def get_chrome_proxy():
    """
    Get proxy settings from Chrome browser

    Returns:
        str or None: Proxy URL if configured, None otherwise
    """
    try:
        # On Windows, check system proxy settings (used by Chrome)
        if platform.system() == "Windows":
            import winreg
            # Check if proxy is enabled
            proxy_enable = winreg.QueryValueEx(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                "ProxyEnable"
            )[0]

            if proxy_enable:
                # Get proxy server
                proxy_server = winreg.QueryValueEx(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                    "ProxyServer"
                )[0]

                if proxy_server:
                    # Proxy server format may be "http=proxy:port;https=proxy:port"
                    # or just "proxy:port"
                    if "=" in proxy_server:
                        # Extract http proxy
                        for part in proxy_server.split(";"):
                            if part.startswith("http="):
                                proxy = part.split("=")[1]
                                return proxy
                    else:
                        return proxy_server

        # On macOS/Linux, could check system proxy settings
        # This is more complex and may not be necessary for most users

        return None
    except Exception as e:
        # Silently fail - proxy is optional
        return None

def detect_clash_proxy():
    """
    Detect Clash proxy by checking common Clash ports

    Returns:
        str or None: Proxy URL if Clash is running, None otherwise
    """
    try:
        # Check Clash ports 7890-7899
        clash_ports = list(range(7890, 7900))  # 7890 to 7899

        for port in clash_ports:
            try:
                # Try to connect to port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    result = s.connect_ex(('127.0.0.1', port))

                    if result == 0:
                        # Port is open - Clash is likely running
                        # Default Clash HTTP proxy is usually 7890
                        # Return HTTP proxy URL
                        return f"http://127.0.0.1:{port}"
            except Exception:
                continue

        return None
    except Exception as e:
        # Silently fail - proxy is optional
        return None

def detect_proxy():
    """
    Detect proxy from multiple sources with priority

    Priority:
    1. Chrome system proxy (if configured)
    2. Clash proxy (if running)

    Returns:
        dict: Proxy information with source and URL, or None
    """
    # Try Chrome proxy first
    proxy = get_chrome_proxy()
    if proxy:
        return {
            "source": "Chrome",
            "url": proxy,
            "description": "Chrome system proxy settings"
        }

    # Try Clash proxy
    proxy = detect_clash_proxy()
    if proxy:
        return {
            "source": "Clash",
            "url": proxy,
            "description": f"Clash proxy (port {proxy.split(':')[-1]})"
        }

    # No proxy found
    return None

def test_youtube_access(proxy=None):
    """
    Test if YouTube is accessible

    Args:
        proxy (str): Proxy URL to use for testing

    Returns:
        dict: Test result with accessible status and info
    """
    import urllib.request
    import urllib.error

    try:
        # Create URL opener with proxy if specified
        if proxy:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener()

        # Test with YouTube main page (timeout 10 seconds)
        request = urllib.request.Request('https://www.youtube.com', headers={'User-Agent': 'Mozilla/5.0'})
        response = opener.open(request, timeout=10)

        # Check if we got a valid response
        if response.getcode() == 200:
            return {
                "accessible": True,
                "proxy_used": proxy if proxy else "Direct",
                "status": "OK"
            }
        else:
            return {
                "accessible": False,
                "proxy_used": proxy if proxy else "Direct",
                "status": f"HTTP {response.getcode()}"
            }
    except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
        return {
            "accessible": False,
            "proxy_used": proxy if proxy else "Direct",
            "status": f"Error: {str(e)[:100]}"
        }

def download_video(url, output_dir=".", format_id="bestvideo+bestaudio/best", cookies_browser=None, **kwargs):
    """
    Download video using yt-dlp

    Args:
        url (str): Video URL
        output_dir (str): Output directory (default: current directory)
        format_id (str): Video format selector (default: bestvideo+bestaudio/best)
        cookies_browser (str): Browser to use for cookies (default: tries 'chrome' if available)
        **kwargs: Additional yt-dlp options

    Returns:
        dict: Download result with status and info
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Build command
    cmd = ["yt-dlp", url]

    # Add format
    cmd.extend(["-f", format_id])

    # Add output directory
    cmd.extend(["-o", f"{output_dir}/%(title)s.%(ext)s"])

    # Use browser cookies (default to chrome for better YouTube support)
    if cookies_browser is None:
        cookies_browser = kwargs.get("cookies_browser", "chrome")

    # Check if cookies_browser is specified and not empty
    use_cookies = cookies_browser and cookies_browser.strip()

    # Get proxy from multiple sources with priority
    manual_proxy = kwargs.get("proxy")
    proxy_url = None
    proxy_info = None

    if manual_proxy:
        proxy_url = manual_proxy
        proxy_info = {
            "source": "Manual",
            "url": manual_proxy,
            "description": "Manually specified proxy"
        }
    else:
        proxy_info = detect_proxy()  # Try Chrome first, then Clash
        proxy_url = proxy_info["url"] if proxy_info else None

    # Test YouTube accessibility if no manual proxy specified
    test_youtube = kwargs.get("test_youtube", True)
    if test_youtube and not manual_proxy:
        print("\n[Testing YouTube accessibility...]")
        test_result = test_youtube_access(proxy_url if proxy_url else None)

        if test_result["accessible"]:
            print(f"[OK] YouTube accessible: {test_result['proxy_used']}")
        else:
            print(f"[FAIL] YouTube not accessible: {test_result['status']}")

            # Try to find a working proxy if direct access fails
            if not proxy_url:
                print("\n[Searching for proxy...]")
                proxy_info = detect_proxy()

                if proxy_info:
                    proxy_url = proxy_info["url"]
                    print(f"[Proxy] Found {proxy_info['source']}: {proxy_url}")
                    print(f"[Proxy] Description: {proxy_info['description']}")

                    # Test with proxy
                    test_result = test_youtube_access(proxy_url)
                    if test_result["accessible"]:
                        print(f"[OK] YouTube accessible via {proxy_info['source']} proxy")
                    else:
                        print(f"[FAIL] Proxy also failed: {test_result['status']}")
                        proxy_url = None
                else:
                    print("[Proxy] No proxy detected (Chrome/Clash not available)")
                    proxy_url = None

    # Add proxy if available
    if proxy_url:
        cmd.extend(["--proxy", proxy_url])

    # Additional options
    if kwargs.get("write_subs"):
        cmd.append("--write-subs")
    if kwargs.get("write_auto_subs"):
        cmd.append("--write-auto-subs")
    if kwargs.get("sub_lang"):
        cmd.extend(["--sub-langs", kwargs["sub_lang"]])
    if kwargs.get("write_description"):
        cmd.append("--write-description")
    if kwargs.get("write_info_json"):
        cmd.append("--write-info-json")
    if kwargs.get("write_thumbnail"):
        cmd.append("--write-thumbnail")
    if kwargs.get("extract_flat"):
        cmd.append("--extract-flat")
    if kwargs.get("playlist_start"):
        cmd.extend(["--playlist-start", str(kwargs["playlist_start"])])
    if kwargs.get("playlist_end"):
        cmd.extend(["--playlist-end", str(kwargs["playlist_end"])])
    if kwargs.get("no_playlists"):
        cmd.append("--no-playlists")
    if kwargs.get("verbose"):
        cmd.append("--verbose")

    # Check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {
            "success": False,
            "error": "yt-dlp is not installed. Please install it with: pip install yt-dlp"
        }

    # Check for existing video file before downloading
    print("\n[Checking for existing files...]")
    try:
        # Extract video ID from URL
        video_id = url.split('=')[-1].split('&')[0]
        
        # List all files in output directory
        existing_files = []
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                if video_id in f:
                    full_path = os.path.join(output_dir, f)
                    existing_files.append(full_path)

        if existing_files:
            print(f"\n[INFO] Found {len(existing_files)} existing file(s) for this video:")
            for f in existing_files:
                try:
                    size = os.path.getsize(f) / 1024 / 1024
                    print(f"  - {os.path.basename(f)} ({size:.2f} MB)")
                except:
                    print(f"  - {os.path.basename(f)}")
            print("\n[INFO] yt-dlp will skip re-download if file already exists.")
            print("[INFO] This is normal behavior to avoid duplicates.")
            print("\n[INFO] To re-download:")
            print("  1. Delete existing file, then try again")
            print("  2. Download to a different directory")
            print("  3. Specify a different output filename")
            print()
    except Exception as e:
        print(f"\n[Warning] Could not check for existing files: {e}")
        print()

    # Execute download with automatic fallback
    try:
        # First try with cookies if enabled
        if use_cookies:
            cmd_with_cookies = cmd.copy()
            cmd_with_cookies.extend(["--cookies-from-browser", cookies_browser])

            result = subprocess.run(
                cmd_with_cookies,
                capture_output=True,
                text=True,
                check=False
            )

            # Check if cookies failed
            if result.returncode != 0 and "Could not copy" in result.stderr and "cookie" in result.stderr.lower():
                # Fallback: retry without cookies
                print(f"Warning: Could not use {cookies_browser} cookies. Retrying without cookies...")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False
                )
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

        if result.returncode == 0:
            return {
                "success": True,
                "message": "Download completed successfully",
                "url": url,
                "output_dir": output_dir
            }
        else:
            return {
                "success": False,
                "error": f"Download failed with return code {result.returncode}",
                "stderr": result.stderr,
                "stdout": result.stdout
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Exception occurred: {str(e)}"
        }

def get_video_info(url, cookies_browser="chrome", proxy=None):
    """
    Get video information without downloading

    Args:
        url (str): Video URL
        cookies_browser (str): Browser to use for cookies (default: 'chrome')
        proxy (str): Proxy URL (default: uses Chrome proxy if available)

    Returns:
        dict: Video information or error
    """
    try:
        # Get proxy if not specified
        if proxy is None:
            proxy = detect_proxy()  # Try Chrome first, then Clash

        # Build command
        cmd = ["yt-dlp", "--dump-json"]
        if proxy:
            cmd.extend(["--proxy", proxy])
        cmd.extend(["--cookies-from-browser", cookies_browser, url])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        info = json.loads(result.stdout)
        return {
            "success": True,
            "info": info
        }
    except subprocess.CalledProcessError as e:
        # Check if cookies failed
        if "Could not copy" in e.stderr and "cookie" in e.stderr.lower():
            # Fallback: retry without cookies
            print(f"Warning: Could not use {cookies_browser} cookies. Retrying without cookies...")
            try:
                cmd = ["yt-dlp", "--dump-json"]
                if proxy:
                    cmd.extend(["--proxy", proxy])
                cmd.append(url)
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                info = json.loads(result.stdout)
                return {
                    "success": True,
                    "info": info
                }
            except subprocess.CalledProcessError as e2:
                return {
                    "success": False,
                    "error": f"Failed to get video info: {e2.stderr}"
                }
        return {
            "success": False,
            "error": f"Failed to get video info: {e.stderr}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse video info: {str(e)}"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "yt-dlp is not installed. Please install it with: pip install yt-dlp"
        }

def list_formats(url, cookies_browser="chrome", proxy=None):
    """
    List available formats for a video

    Args:
        url (str): Video URL
        cookies_browser (str): Browser to use for cookies (default: 'chrome')
        proxy (str): Proxy URL (default: uses Chrome proxy if available)

    Returns:
        dict: Formats list or error
    """
    try:
        # Get proxy if not specified
        if proxy is None:
            proxy = detect_proxy()  # Try Chrome first, then Clash

        # Try with cookies first
        cmd = ["yt-dlp", "--list-formats"]
        if proxy:
            cmd.extend(["--proxy", proxy])
        cmd.extend(["--cookies-from-browser", cookies_browser, url])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        # Check if cookies failed
        if result.returncode != 0 and "Could not copy" in result.stderr and "cookie" in result.stderr.lower():
            # Fallback: retry without cookies
            print(f"Warning: Could not use {cookies_browser} cookies. Retrying without cookies...")
            cmd = ["yt-dlp", "--list-formats"]
            if proxy:
                cmd.extend(["--proxy", proxy])
            cmd.append(url)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

        if result.returncode == 0:
            return {
                "success": True,
                "formats": result.stdout
            }
        else:
            return {
                "success": False,
                "error": result.stderr
            }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "yt-dlp is not installed. Please install it with: pip install yt-dlp"
        }

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python download_video.py <url> [options]")
        print("Example: python download_video.py https://youtube.com/watch?v=xxx")
        sys.exit(1)

    url = sys.argv[1]
    result = download_video(url)

    if result["success"]:
        print(f"✓ Download completed: {result['message']}")
    else:
        print(f"✗ Download failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
