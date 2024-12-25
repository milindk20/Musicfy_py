import os
import yt_dlp

def download_song(song_name, download_folder, ffmpeg_location=None):
    try:
        # Configure yt_dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'quiet': False,
        }
        
        if ffmpeg_location:
            ydl_opts['ffmpeg_location'] = ffmpeg_location
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search and download the first result
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            print(f"Downloaded: {info['entries'][0]['title']}")
    except Exception as e:
        print(f"Failed to download song: {e}")

def main():
    # Prompt user for song name
    song_name = input("Enter the song name: ").strip()
    if not song_name:
        print("Error: Song name cannot be empty.")
        return
    
    # Prompt user for download folder
    #download_folder = input("Enter the download folder path: ").strip()
    download_folder="C:\\Users\\Milind\\Music\\Downloaded"
    download_folder=download_folder.strip()
    if not os.path.isdir(download_folder):
        print("Error: Invalid folder path.")
        return
    
    # Optional: Specify ffmpeg location (update path if necessary)
    ffmpeg_location = r'C:\\Users\\Milind\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1-essentials_build\\bin'
    
    # Call the function to download the song
    download_song(song_name, download_folder, ffmpeg_location)

if __name__ == "__main__":
    main()
