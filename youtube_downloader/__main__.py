from argparse import ArgumentParser
from .controller import main
from pathlib import Path

if __name__ == "__main__":
    parser = ArgumentParser(prog="Youtube Downloader", description="A simple GUI app for downloading videos and mp3s from Youtube with youtube-dl")
    parser.add_argument("-c", "--config", metavar="CONFIG_FILE", action='store_const', const="EMPTY", help="The .cfg file, located in the 'User Options' folder, to load the application with")
    parser.add_argument("-l", "--log", metavar="LOG_FILE", default=str(Path(__file__).parent / "data/stdout.log"), help="The file to log stdout and stderr to")
    args = parser.parse_args()
    
    main(args.config, args.log)