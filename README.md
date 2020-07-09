# youtube-dl
Two simple scripts for downloading from youtube
YT_video_playlist.py downloads specified videos from specified playlists to a specified location
YTMusic_playlist_to_mp3s.py downloads and converts all the videos in the specified youtube playlist to mp3s at the specified location

The example_config.py should be changed to fit your system's location of FFMPEG, and external tool to be downloaded to your machine
Furthermore, the example config can be edited to fit the user's preferences in the areas indicated
Then example_config.py should be renamed to config.py

The scripts automatically update youtube-dl and log to a folder
They will also create the neccesarry files to run if they do not already exists