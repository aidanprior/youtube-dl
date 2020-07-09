from setuptools import setup

setup(
    name='youtube-dl-scripts',
    author="Aidan Prior",
    version='2.0',
    scripts=['shared.py', 'update.py', 'example_config.py', 'YT_video_playlist.py', 'YTMusic_playlist_to_mp3s.py'],
    license='GNU GPL3',
    long_description=open('README.md').read(),
)