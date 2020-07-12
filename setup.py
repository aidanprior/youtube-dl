from setuptools import setup

setup(
    name='youtube-dl-scripts',
    author="Aidan Prior",
    author_email="priorlyaidan@yahoo.com",
    url="https://github.com/aidanprior/youtube-dl",
    version='2.0',
    packages=['youtube-dl-scripts'],
    data_files=[("Logs", ['youtube-dl-scripts/Logs/YT_video_playlists.log', 'youtube-dl-scripts/Logs/YTMusic_playlist_to_mp3s.log', ]),
                ("Archives", ['youtube-dl-scripts/Archives/Audio_Archive.txt', 'youtube-dl-scripts/Archives/Video_Archive.txt', ]),
                ("", ['youtube-dl-scripts/config.ini', ])
                ],
    install_requires = ['youtube_dl',],
    license='GNU GPL3',
)