import sys
import datetime
import winshell

from argparse import ArgumentParser
from pathlib import Path

from .controller import main


if __name__ == "__main__":
    parser = ArgumentParser(prog="Youtube Downloader",
                            description="A simple GUI app for \
                            downloading videos and mp3s from Youtube with \
                            youtube-dl")
    parser.add_argument("-c", "--config", metavar="CONFIG_FILE", const="EMPTY",
                        nargs='?',
                        help="The .cfg file, located in the 'User Options' \
                            folder, to load the application with")
    parser.add_argument("-l", "--log", metavar="LOG_FILE",
                        default=str(Path(winshell.application_data())
                                    / "Youtube Downloader" / "output.log"),
                        help="The file to log stdout and stderr to")
    args = parser.parse_args()

    def full_path_create(p):
        tmp = p.parent
        while not tmp.exists():
            tmp.mkdir()
            tmp = tmp.parent

        if not p.is_dir():
            p.touch(exist_ok=True)

    filepath = Path(args.log)
    full_path_create(filepath)

    sys.stdout = open(filepath, "w")
    sys.stderr = sys.stdout
    x = datetime.datetime.now()

    date_str = (
        f"{x.year}/{x.month}/{x.day}  "
        f"{x.hour:02}:{x.minute:02}:{x.second:02}\n"
    )
    print(date_str)

    main(args.config)
