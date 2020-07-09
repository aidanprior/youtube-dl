import subprocess, sys, importlib

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
    
    version = ''
    return version

