import update, shared

try:
    from config import AUDIO_OUTPUT_LOG_FILE, FFMPEG_BIN_DIR, AUDIO_ARCHIVE_FILE, AUDIO_OUTPUT_TEMPLATE, YTMUSIC_PLAYLIST_URL
except ModuleNotFoundError:
    print("ERROR: config not found")
    print("If this is your first time running this, please make any desired changes to 'example_config.py', and then rename it to 'config.py'")
    input("Press Enter to Exit...")
    exit(1)

lgr = shared.setup_loggers(AUDIO_OUTPUT_LOG_FILE)

#make sure youtube-dl is up to date
youtube_dl = update.update_youtube_dl(True)

#get the playlist's name
with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
    try:
        info = ydl.extract_info(YTMUSIC_PLAYLIST_URL, download=False, process=False)
    except (youtube_dl.utils.DownloadError, youtube_dl.utils.ExtractorError):
        print("ERROR: Playlist URL not valid")
        input("Press Enter to Exit...")
        exit(1)
        

print(f"Downloading from {info.get('_type', '(Unkown)')}: {info.get('title', '(Unknown)')}")
print()

ydl_opts = {
    'verbose': False,
    'noplaylist': False,
    'writethumbnail': True,
    'format': 'bestaudio/best',
    'ffmpeg_location': FFMPEG_BIN_DIR,
    'nooverwrites': True,
    'nopart': True,
    'ignoreerrors': True,
    'outtmpl': AUDIO_OUTPUT_TEMPLATE,
    'download_archive': AUDIO_ARCHIVE_FILE,
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
    'progress_hooks': [shared.create_hook("mB")]
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([YTMUSIC_PLAYLIST_URL])

print()
print("Downloaded %d mp3s" % shared.total_downloaded)
print()
input("Press Enter to Exit...")
