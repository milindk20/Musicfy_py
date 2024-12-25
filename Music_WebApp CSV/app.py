from unittest import result
from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import csv
import yt_dlp
import zipfile
import shutil

app = Flask(__name__)

# Path to save downloaded songs
DOWNLOAD_FOLDER = r"C:\\Users\\Milind\\Music\\Downloaded"
FFMPEG_LOCATION = r'C:\\Users\\Milind\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1-essentials_build\\bin'

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def download_song(track_name, artist_name):
    try:
        search_query = f"{track_name} {artist_name}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'quiet': False,
            'ffmpeg_location': FFMPEG_LOCATION
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{search_query}", download=True)
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{info['entries'][0]['title']}.mp3")
            return file_path, f"{info['entries'][0]['title']}.mp3"
    except Exception as e:
        return None, f"Error: {e}"


def zip_songs(files):
    zip_filename = os.path.join(DOWNLOAD_FOLDER, 'songs.zip')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            try:
                # Decode CSV file content
                file_content = csv_file.read().decode('utf-8', errors='replace')
                rows = []
                reader = csv.DictReader(file_content.splitlines())

                # List to keep track of downloaded files
                downloaded_files = []
                results = []  # Initialize results list here

                for row in reader:
                    track_name = row.get('Track Name', '').strip()
                    artist_name = row.get('Artist Name(s)', '').strip()

                    if track_name and artist_name:
                        file_path, message = download_song(track_name, artist_name)
                        if file_path:
                            downloaded_files.append(file_path)
                        results.append({'track_name': track_name, 'artist_name': artist_name, 'status': 'success' if file_path else 'failed', 'message': message})
                    else:
                        results.append({'track_name': track_name or 'Unknown', 'artist_name': artist_name or 'Unknown', 'status': 'failed', 'message': 'Missing track or artist name'})

                # Once all songs are downloaded, zip them
                if downloaded_files:
                    zip_path = zip_songs(downloaded_files)
                    print(f"ZIPPATH: {zip_path}")
                    # Remove the individual song files after zipping them
                    for file in downloaded_files:
                        os.remove(file)
                    print('sending files')
                    return send_from_directory(DOWNLOAD_FOLDER, 'songs.zip', as_attachment=True)
                else:
                    return jsonify({'status': 'error', 'message': 'No songs were downloaded.'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Failed to process CSV file: {e}'})
        else:
            return jsonify({'status': 'error', 'message': 'No CSV file uploaded.'})
    return render_template('index.html')


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404


if __name__ == '__main__':
    app.run(debug=True)
