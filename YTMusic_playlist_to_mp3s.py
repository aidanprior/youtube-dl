import youtube_dl_wrapper

config = youtube_dl_wrapper.get_config('AUDIO')

TEMPLATE = config['output_dir'] + "/" + config['template']
FFMPEG_BIN_DIR = youtube_dl_wrapper.get_config('SYSTEM')['ffmpeg_bin']
PLAYLIST_URL = "https://music.youtube.com/playlist?list=" + config['playlist_id']

lgr = youtube_dl_wrapper.setup_loggers(__file__)

#make sure youtube-dl is up to date
youtube_dl = youtube_dl_wrapper.update_youtube_dl(True)

#get the archive file
archive = youtube_dl_wrapper.check_archive_file("Audio")

#get the playlist's name
with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
    try:
        info = ydl.extract_info(PLAYLIST_URL, download=False, process=False)
    except (youtube_dl.utils.DownloadError, youtube_dl.utils.ExtractorError):
        print("ERROR: Playlist URL not valid")
        input("Press Enter to Exit...")
        exit(1)
        

print(f"Downloading from {info.get('_type', '(Unkown)')}: {info.get('title', '(Unknown)')}")
print()

#configure the youtube-dl options
ydl_opts = {
    # 'verbose': True,
    'noplaylist': False,
    'writethumbnail': True,
    'format': 'bestaudio/best',
    'ffmpeg_location': FFMPEG_BIN_DIR,
    # 'skip_download': True,
    'nooverwrites': True,
    'nopart': True,
    'ignoreerrors': True,
    'outtmpl': TEMPLATE,
    'download_archive': archive,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }, {
        'key': 'FFmpegMetadata'
    # }, {
    #     'key': 'EmbedThumbnail'
    }],
    'logger': lgr,
    # 'logtostderr': True,
    'progress_hooks': [youtube_dl_wrapper.create_hook("mB")]
}

#download playlist
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([PLAYLIST_URL])

print()
print("Downloaded %d mp3s" % youtube_dl_wrapper.lib.total_downloaded)
print()
input("Press Enter to Exit...")
