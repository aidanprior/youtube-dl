import sys
from pathlib import Path

import shared, update

config = shared.get_config('VIDEO')

INPUT_FILE = config['input_file']
ARCHIVE_FILE = config['archive']
TEMPLATE = config['output_dir'] + "/" + config['template']

PLAYLIST_URL = "https://www.youtube.com/playlist?list="

def download_playlist(playlist_id, start_number, end_number, lgr):
    #get the playlist's name
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(PLAYLIST_URL + playlist_id, download=False, process=False)
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
        'outtmpl': TEMPLATE,
        'download_archive': ARCHIVE_FILE,
        'logger': lgr,
        'progress_hooks': [shared.create_hook("gB")]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([PLAYLIST_URL + playlist_id])

def main():
    global youtube_dl
    lgr = shared.setup_loggers('VIDEO')
    
    #make sure youtube-dl is up to date
    
    youtube_dl = update.update_youtube_dl(True)
    
    if not INPUT_FILE.exists():
        print()
        print(f"Couldn't find the input file: {INPUT_FILE}")
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
                download_playlist(line, int(start_str), int(end_str), lgr)
            place = (place + 1)%2
    
    print()
    print(f"Downloaded {shared.total_downloaded} videos")
    
if __name__ == "__main__":
    main()
    input("Press ENTER to close")