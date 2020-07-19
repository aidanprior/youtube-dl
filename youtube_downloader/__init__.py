from .ui import Ui_MainWindow
from .controller import main
from subprocess import run
import sys
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(prog="Youtube Downloader", description="A simple GUI app for downloading videos and mp3s from Youtube with youtube-dl")
    parser.add_argument("-c", "--config", metavar="CONFIG_FILE", help="The .cfg file to load the application with")
    parser.add_argument("-l", "--log", metavar="LOG_FILE" action='store_const', const="data/stdout.log", help="The file to log stdout and stderr to")
    args = parser.parse_args()
    cmd = [
        sys.executable, 
        "controller.py"
    ]
    if args.config:
        cmd.append("-c")
        cmd.append(args.config)
    cmd.append(">>")
    cmd.append(args.log)
    run(*cmd)