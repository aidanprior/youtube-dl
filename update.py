import subprocess, sys, importlib
from pathlib import Path

def update_youtube_dl(printout):
    if printout:
        print("Checking for the latest youtube-dl version...")
        
    output = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'youtube-dl', '--user'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout_str = output.stdout.decode('utf-8')
    
    if stdout_str[:42] != "Requirement already up-to-date: youtube-dl" and printout:
        print(f"Successfully updated to version ({stdout_str.split('Successfully installed youtube-dl-')[-1].strip()})")
    elif printout:
        print(f"Already up to date with version ({stdout_str[108:].split(')')[0]})")
       
    return importlib.import_module('youtube_dl')

def update_this():
    RELEASE = 'origin/master'
    SRC_DIR = Path(__file__).parent.resolve()
    CMD = (
    f'pip install --src="{SRC_DIR}" --upgrade -e ' 
    f'git://github.com/awp95/youtube-dl.git@{RELEASE}#egg=youtube-dl' 
    )
    CMD = (
    f'pip install --src="{SRC_DIR}" --upgrade ' 
    f'https://github.com/awp95/youtube-dl/dist/master.zip' 
    )

    subprocess.check_call(CMD)


if __name__ == "__main__":
    update_youtube_dl(True)
    update_this()