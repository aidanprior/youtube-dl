from subprocess import check_call
import sys
from argparse import ArgumentParser
from pathlib import Path

if __name__ == "__main__":
    parser = ArgumentParser(prog="Youtube Downloader", description="A simple GUI app for downloading videos and mp3s from Youtube with youtube-dl")
    parser.add_argument("-c", "--config", metavar="CONFIG_FILE", help="The .cfg file to load the application with")
    parser.add_argument("-l", "--log", metavar="LOG_FILE", default="data/stdout.log", help="The file to log stdout and stderr to")
    args = parser.parse_args()
    
    parent = Path(__file__).parent
    
    cmd = [
        "python", 
        str(parent / "controller.py")
    ]
    if args.config != None:
        cmd.append("-c")
        cmd.append(str(parent / args.config))
    # cmd.append(">>")
    # cmd.append(str(parent / args.log))
    cmd_str = " ".join(cmd)
    check_call(cmd_str)