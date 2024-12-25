import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp

def download_song():
    song_name = entry.get()
    if not song_name:
        messagebox.showerror("Error", "Please enter a song name.")
        return
    
    # Prompt the user to select a download folder
    download_folder = filedialog.askdirectory(title="Select Download Folder")
    if not download_folder:
        messagebox.showerror("Error", "No folder selected for download.")
        return
    
    try:
        # Configure yt_dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'quiet': False,
            'ffmpeg_location': r'C:\\Users\\Milind\\AppData\\Local\\Microsoft\WinGet\\Packages\\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1-essentials_build\bin'  # Replace with the actual path to FFmpeg
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Use yt_dlp to search and download the first result
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            messagebox.showinfo("Success", f"Downloaded: {info['entries'][0]['title']}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download song. {e}")

# Create the GUI
root = tk.Tk()
root.title("Song Downloader")

tk.Label(root, text="Enter Song Name:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="Download", command=download_song).pack(pady=20)

root.mainloop()
