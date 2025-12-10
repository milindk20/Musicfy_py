# Musicfy_py

Lightweight web UI and CLI utilities to search and download audio from YouTube (via yt-dlp), convert to MP3 (FFmpeg), and serve downloads. Includes single-song download, CSV-batch download, ZIP export and a housekeeping daemon for cleaning old files.

## Quick links
- Files in this repo:
  - [master_launcher.py](master_launcher.py)
  - [housekeeping_linux.py](housekeeping_linux.py)
  - [Linux/app_combined.py](Linux/app_combined.py)
  - [Linux/config.py](Linux/config.py)
  - [Linux/requirements.txt](Linux/requirements.txt)
  - [Linux/templates/index.html](Linux/templates/index.html)
  - [Windows/app_combined.py](Windows/app_combined.py)
  - [Windows/config.py](Windows/config.py)
  - [Windows/templates/index.html](Windows/templates/index.html)
  - [Server/initialize.sh](Server/initialize.sh)
  - [Server/start_app.sh](Server/start_app.sh)
  - [TEST/check_datetime.py](TEST/check_datetime.py)
  - [TEST/Music_GUI_1_Song.py](TEST/Music_GUI_1_Song.py)
  - [TEST/Music.py](TEST/Music.py)

- Important symbols:
  - [`master_launcher.main`](master_launcher.py)
  - [`housekeeping_linux.remove_old_files`](housekeeping_linux.py)
  - [`Linux.config.DOWNLOAD_FOLDER`](Linux/config.py)
  - [`Linux.config.FFMPEG_LOCATION`](Linux/config.py)
  - [`Linux.app_combined.download_song`](Linux/app_combined.py)
  - [`Linux.app_combined.zip_songs`](Linux/app_combined.py)
  - [`Windows.app_combined.download_song`](Windows/app_combined.py)

## Requirements
- Python 3.8+
- FFmpeg (path configurable in `Linux/config.py` and `Windows/config.py`)
- System packages (see [Server/initialize.sh](Server/initialize.sh))
- Python packages: see [Linux/requirements.txt](Linux/requirements.txt)

## Setup (server / VM)
1. Clone repo:
   git clone https://github.com/milindk20/Musicfy_py.git
2. On server, run the initializer (creates venv, installs deps):
   bash Musicfy_py/Server/initialize.sh
   - This script installs requirements from [Linux/requirements.txt](Linux/requirements.txt) and prepares the environment.
3. Start app + housekeeping (the initializer copies and prepares start script):
   /data/start_app.sh
   - See [Server/start_app.sh](Server/start_app.sh) to understand how `master_launcher.py` and `housekeeping_linux.py` are launched.

## Run locally (development)
- Linux:
  - Ensure Python venv active and dependencies installed:
    pip install -r Linux/requirements.txt
  - Run:
    python Linux/app_combined.py
- Windows:
  - Run:
    python Windows/app_combined.py
- Or use the launcher which selects by OS: [`master_launcher.main`](master_launcher.py)

App listens on port 5000 by default (Linux app sets host `0.0.0.0`).

## Usage (web UI)
- Open: http://<host>:5000
- Single song:
  - Enter a song name and Submit. The server will search YouTube and return a downloadable MP3.
- CSV batch:
  - Upload a CSV containing two columns EXACTLY named:
    - `Track Name`
    - `Artist Name(s)`
  - The server processes each row, downloads songs, and the UI provides status for each download and a link to download `all-songs.zip`.
- Templates:
  - Linux UI: [Linux/templates/index.html](Linux/templates/index.html)
  - Windows UI: [Windows/templates/index.html](Windows/templates/index.html)

## How downloads are stored & configuration
- Linux download location: [`DOWNLOAD_FOLDER` in Linux/config.py](Linux/config.py)
- Windows download location: [`DOWNLOAD_FOLDER` in Windows/config.py](Windows/config.py)
- FFmpeg path is configured via `FFMPEG_LOCATION` in each config file:
  - [`Linux.config.FFMPEG_LOCATION`](Linux/config.py)
  - [`Windows.config.FFMPEG_LOCATION`](Windows/config.py)

## Endpoints (server)
- GET / -> HTML UI (rendered template)
- POST / -> start a single-song download or process uploaded CSV (as in [Linux/app_combined.py](Linux/app_combined.py) and [Windows/app_combined.py](Windows/app_combined.py))
- GET /download/<filename> -> downloads a single file (see [`download_file`](Linux/app_combined.py))
- GET /download/all-songs.zip -> returns zip created by [`zip_songs`](Linux/app_combined.py)

## Housekeeping
- Housekeeping is launched by [Server/start_app.sh](Server/start_app.sh) via:
  nohup python3 ./housekeeping_linux.py ...
- The cleaner function is [`housekeeping_linux.remove_old_files`](housekeeping_linux.py). Note: there's a bug in `TIME_THRESHOLD` in that file (it multiplies by 60 one time too many). Consider fixing to:


See [housekeeping_linux.py](housekeeping_linux.py).

## Common troubleshooting
- yt-dlp fails to extract or FFmpeg errors:
- Verify `FFMPEG_LOCATION` points to a working ffmpeg binary.
- Check permissions of `DOWNLOAD_FOLDER`.
- No files after download:
- The app writes temp output with timestamped template then renames to sanitized title; check console logs and [Linux/app_combined.py](Linux/app_combined.py) for renaming logic.
- CSV parsing issues:
- Ensure CSV column headers match exactly `Track Name` and `Artist Name(s)`.

## Testing & utilities
- GUI single-song tester: [TEST/Music_GUI_1_Song.py](TEST/Music_GUI_1_Song.py)
- CLI tester: [TEST/Music.py](TEST/Music.py)
- Filename sanitization helper example: [TEST/check_datetime.py](TEST/check_datetime.py)

## Contributing
- Fork, branch, open PR.
- Keep cross-platform config separate in `Linux/` and `Windows/`.

