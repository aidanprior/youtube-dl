import sys
from pathlib import Path

import shared, update
try:
    from config import VIDEO_INPUT_FILE, VIDEO_ARCHIVE_FILE, VIDEO_OUTPUT_DIR, VIDEO_OUTPUT_LOG_FILE, VIDEO_OUTPUT_TEMPLATE, PLAYLIST_URL_FIRST_HALF
except ModuleNotFoundError:
    print("ERROR: config not found")
    print("If this is your first time running this, please make any desired changes to 'example_config.py', and then rename it to 'config.py'")
    input("Press Enter to Exit...")
    exit(1)

def download_playlist(playlist_id, start_number, end_number, lgr):
    #get the playlist's name
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(PLAYLIST_URL_FIRST_HALF + playlist_id, download=False, process=False)
    print(f"Downloading from {info.get('_type', '(Unkown)')}: {info.get('title', '(Unknown)')}")

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
        'outtmpl': VIDEO_OUTPUT_TEMPLATE,
        'download_archive': VIDEO_ARCHIVE_FILE,
        'logger': lgr,
        'progress_hooks': [shared.create_hook("gB")]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([PLAYLIST_URL_FIRST_HALF + playlist_id])

def main():
    global youtube_dl
    lgr = shared.setup_loggers(VIDEO_OUTPUT_LOG_FILE)
    
    #make sure youtube-dl is up to date
    
    youtube_dl = update.update_youtube_dl(True)
    
    if not VIDEO_INPUT_FILE.exists():
        print()
        print(f"Couldn't find the input file: {VIDEO_INPUT_FILE}")
        print()
        input("Press ENTER to close")
        sys.exit(1)
    
    with Path(VIDEO_INPUT_FILE).open() as input_file:
        place = 0
        for line in input_file:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            if place == 0:
                start_str, end_str = line.split('-')
            elif place == 1:
                download_playlist(line, int(start_str), int(end_str), lgr)
            place = (place + 1)%2
    
    print()
    print(f"Downloaded {shared.total_downloaded} videos")
    
if __name__ == "__main__":
    main()
    input("Press ENTER to close")