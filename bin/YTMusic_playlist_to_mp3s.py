import update, shared
from config import AUDIO_OUTPUT_LOG_FILE, FFMPEG_BIN_DIR, AUDIO_ARCHIVE_FILE, AUDIO_OUTPUT_TEMPLATE, YTMUSIC_PLAYLIST_URL

lgr = shared.setup_loggers(AUDIO_OUTPUT_LOG_FILE)

#make sure youtube-dl is up to date
youtube_dl = update.update_youtube_dl(True)

#get the playlist's name
with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info(YTMUSIC_PLAYLIST_URL, download=False, process=False)

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
