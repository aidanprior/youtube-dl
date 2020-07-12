from setuptools import setup

setup(
    name='youtube-dl-scripts',
    author="Aidan Prior",
    author_email="priorlyaidan@yahoo.com",
    url="https://github.com/aidanprior/youtube-dl",
    version='2.0',
    packages=['youtube-dl-scripts'],
    package_dir={'youtube-dl-scripts': "youtube-dl-scripts"},
    package_data={'youtube-dl-scripts': [
        'Logs/YT_video_playlists.log', 
        'Logs/YTMusic_playlist_to_mp3s.log', 
        'Archives/Audio_Archive.txt', 
        'Archives/Video_Archive.txt', 
        'config.ini'
        ]},
    install_requires = ['youtube_dl',],
    license='GNU GPL3',
)