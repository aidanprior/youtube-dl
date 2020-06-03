import youtube_dl, logging, subprocess, sys
from pathlib import Path

# ----- CONFIGURATION STUFF ----
# !!! DON'T CHANGE THIS STUFF !!!
# FYI: Directory is another term for a folder, and is often shortened to Dir

HOME = Path.home() # This is the user's directory. ie. "C:/Users/Johnny" on Windows
                   # It can be joined with another path like so HOME / "Desktop/New Folder"
THIS_DIR = Path(__file__).parent.resolve() # This is the directory where this script is

# YOU MAY CHANGE THIS STUFF
# FILE PATHS CAN'T USE BACKSLASHES! Change "C:\blah\blah\blah" to "C:/blah/blah/blah"
OUTPUT_DIR = HOME / "Downloads/mp3s"
OUTPUT_TEMPLATE = "%(title)s.%(ext)s"

YTMUSIC_PLAYLIST_URL = "https://music.youtube.com/playlist?list=PLhJkIvP92dx7NIlyQIacAjbiNgakqPZQ_"

OUTPUT_LOG_FILE = THIS_DIR / "Logs/YTMusic_playlist_to_mp3s.log"
ARCHIVE_FILE = THIS_DIR / "Archives/Audio_Archive.txt"
FFMPEG_BIN_DIR = Path("C:/Program Files/ffmpeg-20200601-dd76226-win64-static/bin")


# !!! DON'T CHANGE ANYTHING BELOW HERE !!!
c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(filename)s : %(lineno)d - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
c_handler.setLevel(logging.WARNING)

f_handler = logging.FileHandler(OUTPUT_LOG_FILE.resolve())
f_format = logging.Formatter('%(asctime)s - %(filename)s : %(lineno)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
f_handler.setFormatter(f_format)
f_handler.setLevel(logging.DEBUG)

lgr = logging.getLogger(__name__)
lgr.addHandler(c_handler)
lgr.addHandler(f_handler)

total_downloaded = 0
def progress_hook(d):
    global total_downloaded
    if d['status'] == 'finished'and d.get('filename', False):
        kB = -1
        mins = 0
        secs = 0
        if d.get('downloaded_bytes', None):
            kB = d['downloaded_bytes']/1024
        if d.get('elapsed', 0):
            mins = d['elapsed']//60
            secs = d['elapsed']%60
        
        print("Downloaded: %-32.31s%4.2fmB%2d:%02d" % (Path(d['filename']).stem, kB, mins, secs), end=("\t" * 20))
        total_downloaded += 1
    
    elif d['status'] == 'downloading' and d.get('filename', False):
        percent_progress = -1
        kBs = -1
        if d.get('downloaded_bytes', None) and d.get('total_bytes', None):
            percent_progress = int(d['downloaded_bytes']/d['total_bytes']*100)
        if d.get('speed', None):
            kBs = int(d['speed']/1024)

        progress_str = ' ' * len('downloaded: ') + "%-27.26s%6d%% %5dkB/s ETA: %2ds%30s" % (Path(d['filename']).stem, percent_progress, kBs, d.get('eta', -1), " ")
        print(f'{progress_str}\r', end="")

ydl_opts = {
    'verbose': False,
    'noplaylist': False,
    'writethumbnail': True,
    'format': 'bestaudio/best',
    'ffmpeg_location': str(FFMPEG_BIN_DIR.resolve()),
    'nooverwrites': True,
    'nopart': True,
    'ignoreerrors': True,
    'outtmpl': str((OUTPUT_DIR / OUTPUT_TEMPLATE).resolve()),
    'download_archive': str(ARCHIVE_FILE.resolve()),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }, {
        'key': 'FFmpegMetadata'
    }, {
        'key': 'EmbedThumbnail'
    }],
    'logger': lgr,
    'progress_hooks': [progress_hook]
}

print("Checking for the latest version...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'youtube-dl', '--user'], stdout=subprocess.DEVNULL)

print("Downloading from playlist id= %s" % YTMUSIC_PLAYLIST_URL.split('playlist?list=')[-1])
print()

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([YTMUSIC_PLAYLIST_URL])

print()
print("Downloaded %d mp3s" % total_downloaded)
input()