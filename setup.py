import setuptools
setuptools.setup()

import platform
if platform.system() == 'Windows':
    import winshell
    from win32com.client import Dispatch
    from pathlib import Path
    desktop = winshell.desktop()
    shell = Dispatch('WScript.Shell')
    
    shortcut = shell.CreateShortCut(str(Path(desktop) / "Youtube Downloader.lnk"))
    shortcut.Targetpath = str(Path("C:/Program Files (x86)/Python38-32/pythonw.exe")) 
    shortcut.Arguments = '-m youtube_downloader -c'
    shortcut.WorkingDirectory = str(Path.home())
    shortcut.save()