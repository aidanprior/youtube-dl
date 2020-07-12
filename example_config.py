#!!!! DON'T TOUCH !!!!
from pathlib import Path
HOME = Path.home()
THIS_DIR = Path(__file__).parent.resolve()






#---- CONFIGURABLE ----

#SYSTEM
FFMPEG_BIN_DIR = Path("C:/Program Files (x86)/ffmpeg-20200628-4cfcfb3-win64-static/bin").resolve()
PLAYLIST_URL_FIRST_HALF = "https://www.youtube.com/playlist?list="

#USER PREFERENCES:
AUDIO_OUTPUT_DIR = HOME / "Downloads/mp3s"
AUDIO_OUTPUT_SHORT_TEMPLATE = "%(title)s.%(ext)s"
YTMUSIC_PLAYLIST_URL = "https://music.youtube.com/playlist?list=lkasjdfioAIEaldks8"

AUDIO_OUTPUT_LOG_FILE = THIS_DIR / "Logs/YTMusic_playlist_to_mp3s.log"
AUDIO_ARCHIVE_FILE = THIS_DIR / "Archives/Audio_Archive.txt"

VIDEO_OUTPUT_DIR = HOME / "Videos/Youtube"
VIDEO_INPUT_FILE = VIDEO_OUTPUT_DIR / "Playlists.txt"
VIDEO_OUTPUT_SHORT_TEMPLATE = "%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s"

VIDEO_OUTPUT_LOG_FILE = THIS_DIR / "Logs/YT_video_playlists.log"
VIDEO_ARCHIVE_FILE = THIS_DIR / "Archives/Video_Archive.txt"






#!!!! DON'T TOUCH !!!!
def check_create_tree(filepath):
    if not filepath.exists():
        #build tree
        to_make = filepath.parent
        while True:
            try:
                Path.mkdir(to_make)
            except FileExistsError:
                break
            to_make = to_make.parent
        Path.touch(filepath, exist_ok=True)

check_create_tree(AUDIO_ARCHIVE_FILE)
check_create_tree(VIDEO_ARCHIVE_FILE)
check_create_tree(AUDIO_OUTPUT_LOG_FILE)
check_create_tree(VIDEO_OUTPUT_LOG_FILE)
check_create_tree(VIDEO_INPUT_FILE)

FFMPEG_BIN_DIR = str(FFMPEG_BIN_DIR.resolve())
AUDIO_OUTPUT_TEMPLATE = str((AUDIO_OUTPUT_DIR / AUDIO_OUTPUT_SHORT_TEMPLATE).resolve())
AUDIO_ARCHIVE_FILE = str(AUDIO_ARCHIVE_FILE.resolve())
AUDIO_OUTPUT_LOG_FILE.resolve()

VIDEO_OUTPUT_TEMPLATE = str((VIDEO_OUTPUT_DIR / VIDEO_OUTPUT_SHORT_TEMPLATE).resolve())
VIDEO_ARCHIVE_FILE = str(VIDEO_ARCHIVE_FILE.resolve())
VIDEO_OUTPUT_LOG_FILE.resolve()