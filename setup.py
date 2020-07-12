from setuptools import setup

setup(
    name='youtube-dl-scripts',
    author="Aidan Prior",
    author_email="priorlyaidan@yahoo.com",
    url="https://github.com/aidanprior/youtube-dl",
    version='2.0',
    packages=['youtube-dl-scripts'],
    data_files=[("youtube-dl-scripts/Logs", ['YT_video_playlists.log', 'YTMusic_playlist_to_mp3s.log', ]),
                ("youtube-dl-scripts/Logs", ['Audio_Archive.txt', 'Video_Archive.txt', ]),
                ("youtube-dl-scripts", ['config.cfg', ])
                ],
    install_requires = ['youtube_dl',],
    license='GNU GPL3',
)