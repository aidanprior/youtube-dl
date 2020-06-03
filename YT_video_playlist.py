import youtube_dl, logging, subprocess, sys
from pathlib import Path

# ----- CONFIGURATION STUFF ----
# !!! DON'T CHANGE THIS STUFF !!!
# FYI: Directory is another term for a folder, and is often shortened to Dir
HOME = Path.home() # This is the user's directory. ie. "C:/Users/Johnny" on Windows
                   # It can be joined with another path like so: HOME / "Desktop/New Folder"
THIS_DIR = Path(__file__).parent.resolve() # This is the directory where this script is

# YOU MAY CHANGE THIS STUFF
# FILE PATHS CAN'T USE BACKSLASHES! Change "C:\blah\blah\blah" to "C:/blah/blah/blah"
PRINT_PLAYLIST_TITLES = False # Do you want to print the titles of the playlists, this may take a bit more time, 
                              # its not really worth it with the output template you are using

OUTPUT_DIR = HOME / "Videos/Youtube"
OUTPUT_TEMPLATE = "%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"

OUTPUT_LOG_FILE = THIS_DIR / "Logs/YT_video_playlists.log"
ARCHIVE_FILE = THIS_DIR / "Archives/Video_Archive.txt"

INPUT_FILE = HOME / "AppData/youtube-dl/Playlists.txt" # This is where your old one is, but I would suggest using the one below
# INPUT_FILE = OUTPUT_DIR / "Playlists.txt"
PATH_FIRST_HALF = "https://www.youtube.com/playlist?list="


# !!! DON'T CHANGE ANYTHING BELOW HERE !!!
c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(filename)s : %(lineno)d - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
c_handler.setLevel(logging.CRITICAL)

f_handler = logging.FileHandler(OUTPUT_LOG_FILE)
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
        mB = -1
        mins = 0
        secs = 0
        if d.get('downloaded_bytes', 0):
            mB = d['downloaded_bytes']/1024/1024
        if d.get('elapsed', 0):
            mins = d['elapsed']//60
            secs = d['elapsed']%60
        
        print("Downloaded: %-32.31s%3.2fmB%2d:%02d" % (Path(d['filename']).stem, mB, mins, secs), end=("\t" * 20))
        total_downloaded += 1
    
    elif d['status'] == 'downloading' and d.get('filename', False):
        percent_progress = -1
        kBs = -1
        eta = -1
        if d.get('downloaded_bytes', 0) and d.get('total_bytes', 0):
            percent_progress = int(d['downloaded_bytes']/d['total_bytes']*100)
        if d.get('speed', 0):
            kBs = int(d['speed']/1024)
        if d.get('eta', 0):
            eta = d['eta']

        progress_str = ' ' * len('downloaded: ') + "%-27.26s%6d%% %5dkB/s ETA: %2ds%30s" % (Path(d['filename']).stem, percent_progress, kBs, eta, " ")
        print(f'{progress_str}\r', end="")

def get_title(playlist_id):
    with youtube_dl.YoutubeDL({'logger': lgr, 'simulate': True, 'skip_download': True}) as ydl:
        output = ydl.extract_info(PATH_FIRST_HALF + playlist_id, download=False)
    print("Downloading from: %s" % output.get('title', "(No Playlist Title Found!)"))

def download_playlist(playlist_id, start_number, end_number):
    if PRINT_PLAYLIST_TITLES:
        get_title(playlist_id)
    else:
        print("Downloading playlist with id=", playlist_id)

    ydl_opts = {
        'verbose': False,
        'noplaylist': False,
        'ignoreerrors': True,
        # skip_download': True,
        'merge_output_format': "mkv",
        'video_format': "mkv",
        'nooverwrites': True,
        'playliststart': start_number,
        'playlistend': end_number,
        'outtmpl': str((OUTPUT_DIR / OUTPUT_TEMPLATE).resolve()),
        'download_archive': str(ARCHIVE_FILE.resolve()),
        'logger': lgr,
        'progress_hooks': [progress_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([PATH_FIRST_HALF + playlist_id])

if __name__ == "__main__":
    print(OUTPUT_LOG_FILE)
    print("Checking for the latest version...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'youtube-dl', '--user'], stdout=subprocess.DEVNULL)

    if not INPUT_FILE.exists():
        print()
        print("Couldn't find the input file: (%s)" % str(INPUT_FILE))
        print()
        input("Press ENTER to close")
        sys.exit(1)
    

    with Path(INPUT_FILE).open() as input_file:
        place = 0
        for line in input_file:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            if place == 0:
                start_str, end_str = line.split('-')
            elif place == 1:
                download_playlist(line, int(start_str), int(end_str))
            place = (place + 1)%2
    print()
    print("Downloaded %d videos" % total_downloaded)
    input("Press ENTER to close")