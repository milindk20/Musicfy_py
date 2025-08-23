# Path to the folder where downloaded files will be stored
from os import environ, path

HOME = environ["HOME"]
DOWNLOAD_FOLDER = path.join(HOME, 'Downloads/Music/')

# Path to the ffmpeg binary
FFMPEG_LOCATION = '/usr/bin/ffmpeg'

