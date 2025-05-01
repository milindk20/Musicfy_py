from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import csv
import yt_dlp

app = Flask(__name__)

# Path to save downloaded songs
DOWNLOAD_FOLDER = r"C:\\Users\\Milind\\Music\\Downloaded"
FFMPEG_LOCATION = r'C:\\Users\\Milind\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1-essentials_build\\bin'

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_song(search_query):
    try:
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

                for row in reader:
                    rows.append(row)

                # Process each song in the CSV
                results = []
                for row in rows:
                    track_name = row.get('Track Name', '').strip()
                    artist_name = row.get('Artist Name(s)', '').strip()

                    if track_name and artist_name:
                        search_query = f"{track_name} {artist_name}"
                        file_path, message = download_song(search_query)
                        results.append({'track_name': track_name, 'artist_name': artist_name, 'status': 'success' if file_path else 'failed', 'message': message})
                    else:
                        results.append({'track_name': track_name or 'Unknown', 'artist_name': artist_name or 'Unknown', 'status': 'failed', 'message': 'Missing track or artist name'})

                return jsonify(results)
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Failed to process CSV file: {e}'})
        else:
            song_name = request.form.get('song_name')
            if not song_name:
                return jsonify({'status': 'error', 'message': 'Please enter a song name.'})

            file_path, message = download_song(song_name)
            if not file_path:
                return jsonify({'status': 'error', 'message': message})

            return jsonify({'status': 'success', 'file_name': message})
    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404
    
import zipfile

def zip_songs():
    # Define the path for the ZIP file
    zip_path = os.path.join(DOWNLOAD_FOLDER, 'all-songs.zip')

    try:
        # Create the ZIP file
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(DOWNLOAD_FOLDER):
                # Only add MP3 files to the ZIP
                if file.endswith('.mp3'):
                    file_path = os.path.join(DOWNLOAD_FOLDER, file)
                    zipf.write(file_path, arcname=file)  # Add file with its name
        return zip_path
    except Exception as e:
        return None, str(e)


@app.route('/download/all-songs.zip', methods=['GET'])
def download_all_songs():
    print('in daz')
    try:
        print('in tryzip')
        zip_path = zip_songs()
        print('in outzip returing zip')
        return send_from_directory(DOWNLOAD_FOLDER, 'all-songs.zip', as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 404


if __name__ == '__main__':
    app.run(debug=True)
