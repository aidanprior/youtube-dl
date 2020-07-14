import subprocess, sys, importlib


def update_youtube_dl(printout):
    if printout:
        print("Checking for the latest youtube-dl version...")
        
    output = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'youtube-dl'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout_str = output.stdout.decode('utf-8').split("Defaulting to user installation because normal site-packages is not writeable\r\n")[-1]
    
    if stdout_str[:42] != "Requirement already up-to-date: youtube-dl" and printout:
        print(f"Successfully updated to version ({stdout_str.split('Successfully installed youtube-dl-')[-1].strip()})")
    elif printout:
        print(f"Already up to date with version ({stdout_str[108:].split(')')[0]})")
        
    return importlib.import_module('youtube_dl')

def update_this():
    cmd = (
    f'python -m pip install --upgrade ' 
    f'https://github.com/aidanprior/youtube-dl/archive/master.zip'
    )

    subprocess.check_call(cmd)

if __name__ == "__main__":
    update_this()