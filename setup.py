import setuptools
import platform

setuptools.setup()

if platform.system() == 'Windows':
    import winshell
    from pathlib import Path
    from site import USER_SITE
    from sys import exec_prefix
    desktop = Path(winshell.desktop())

    with winshell.shortcut(str(desktop / "Youtube Downloader.lnk")) \
            as shortcut:
        shortcut.path = str(Path(exec_prefix) / "pythonw.exe")
        icon = USER_SITE + "\\youtube_downloader\\icon.ico", 0
        shortcut.icon_location = icon
        shortcut.description = "A Youtube Downloader GUI Application"
        shortcut.arguments = '-m youtube_downloader -c'
        shortcut.working_directory = str(Path.home())
