import os
import time
from datetime import datetime, timedelta
from Linux.config import DOWNLOAD_FOLDER  # type: ignore

# Path to the download folder

# Time threshold for file deletion (24 hours in seconds)
TIME_THRESHOLD = 24 * 60 * 60 * 60  # 24 hours

def remove_old_files(folder_path, time_threshold):
    try:
        current_time = time.time()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # Get the file's last modification time
                file_mod_time = os.path.getmtime(file_path)
                # Check if the file is older than the threshold
                print(current_time, file_mod_time, time_threshold)
                print(f"Current time: {current_time}, File modification time: {file_mod_time}","difference:", current_time - file_mod_time)
                print(f"Time threshold: {time_threshold}")
                if current_time - file_mod_time > time_threshold:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
    except Exception as e:
        print(f"Error during housekeeping: {e}")

if __name__ == "__main__":
    print(f"Running housekeeping for folder: {DOWNLOAD_FOLDER}")
    remove_old_files(DOWNLOAD_FOLDER, TIME_THRESHOLD)
