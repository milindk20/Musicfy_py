from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import yt_dlp

app = Flask(__name__)

# Path to save downloaded songs
DOWNLOAD_FOLDER = r"C:\\Users\\Milind\\Music\\Downloaded"
FFMPEG_LOCATION = r'C:\\Users\\Milind\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1-essentials_build\\bin'

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_song(song_name):
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
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{info['entries'][0]['title']}.mp3")
            return file_path, f"{info['entries'][0]['title']}.mp3"
    except Exception as e:
        return None, f"Error: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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

if __name__ == '__main__':
    app.run(debug=True)
