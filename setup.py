from setuptools import setup

setup(
    name='youtube-dl-scripts',
    author="Aidan Prior",
    author_email="priorlyaidan@yahoo.com",
    url="https://github.com/aidanprior/youtube-dl",
    version='2.0',
    scripts=['setup.py', 'shared.py', 'update.py', 'example_config.py', 'YT_video_playlist.py', 'YTMusic_playlist_to_mp3s.py'],
    license='GNU GPL3',
)