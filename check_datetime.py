from datetime import  datetime
from werkzeug.utils import secure_filename
import os

DOWNLOAD_FOLDER = r"/home/milind/Downloads"

original_outtmpl = "musicDownloaded_2025-05-01-20-10-43"
sanitized_outtmpl = secure_filename(original_outtmpl+".mp3")
outtmpl = os.path.join(DOWNLOAD_FOLDER, sanitized_outtmpl)
print(original_outtmpl)
print(sanitized_outtmpl)
print(outtmpl)
file_path="/home/milind/Downloads/LYRICAL_Kaise_Mujhe__Ghajini__Aamir_Khan_Asin__Benny_Dayal_Shreya_Ghosal__A.R._Rahman.mp3"
if os.path.exists(outtmpl):
    print("exists")
    os.rename(outtmpl, file_path)
