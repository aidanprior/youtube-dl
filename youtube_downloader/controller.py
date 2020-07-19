import sys
import youtube_dl
import datetime

from pathlib import Path
from configparser import ConfigParser
from argparse import ArgumentParser

from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from PyQt5.QtCore import QDir, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from .ui import Ui_MainWindow
from .update import update_youtube_dl

class Download_Thread(QThread):
    
    eta_signal = pyqtSignal(str)
    speed_signal = pyqtSignal(str)
    percent_signal = pyqtSignal(int)
    filename_signal = pyqtSignal(str)
    list_item_string_signal = pyqtSignal(str)
    finished_downloading_signal = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Download_Thread, self).__init__(parent=parent)
        self.emittedFilename = False

    def fill(self, url, options):
        self.url = url
        self.options = options
        self.emittedFilename = False
        
    def run(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            output = ydl.download([self.url])
        self.finished_downloading_signal.emit(output)
        
            
                    

class Ui_Controller():
    def __init__(self, start_config=None):
        self._create_dirs()
        
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.MainWindow.setWindowIcon(QIcon("data/icon.ico"))
        self.ui = Ui_MainWindow()
                
        self.download_thread = Download_Thread()
        
        self.ui.setupUi(self.MainWindow)
        self._setup_connections()
        
        if start_config == None:
            self._load_options(self.default_config_location)
        elif not (self.user_options_dir / start_config).exists():
            raise Exception("Passed Config File Path doesn't exist!")
        else:
             self._load_options(self.user_options_dir / start_config)
             
        update_youtube_dl(True)
        
    
    def _create_dirs(self):
        self.data_dir = Path(__file__).parent / 'data'
        self.archive_dir = self.data_dir / 'archives'
        self.user_options_dir = self.data_dir / 'User Options'
        self.plist_inputs_dir = self.data_dir / 'Multi-Playlist Configs'
        self.default_config_location = self.data_dir / "last_opened_options.cfg"
        
        self.archive_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        self.user_options_dir.mkdir(exist_ok=True)
        self.plist_inputs_dir.mkdir(exist_ok=True)
    
    
    def _setup_connections(self):
        get_download_folder = lambda: self.ui.download_folder_input.setText(
            QFileDialog.getExistingDirectory(self.MainWindow, "Set Download Folder", (Path.home()/'Downloads').as_posix()))
        self.ui.download_folder_browse_button.clicked.connect(get_download_folder)
        
        get_ffmpeg_bin = lambda: self.ui.ffmpeg_bin_input.setText(
            QFileDialog.getExistingDirectory(self.MainWindow, "Set FFmpeg Bin", QDir.rootPath()))
        self.ui.ffmpeg_bin_browse_button.clicked.connect(get_ffmpeg_bin)
        
        get_plists_file = lambda: self.ui.plists_file_input.setText(
            QFileDialog.getOpenFileName(self.MainWindow, "Load Multi-Playlist Config", str(self.plist_inputs_dir),  
                                        "Config Files (*.cfg)", options= QFileDialog.Options()))
        self.ui.plists_file_browse_button.clicked.connect(get_plists_file)
        
        self.ui.load_options_button.clicked.connect(lambda: self._load_options())
        self.ui.save_options_button.clicked.connect(lambda: self._save_options())
        
        self.ui.download_now_button.clicked.connect(self._start_download)
        
        self.download_thread.eta_signal.connect(self.ui.eta_label.setText)
        self.download_thread.speed_signal.connect(self.ui.speed_label.setText)
        self.download_thread.percent_signal.connect(self.ui.download_progressbar.setValue)
        self.download_thread.filename_signal.connect(self.ui.download_filename_label.setText)
        self.download_thread.list_item_string_signal.connect(self.ui.downloaded_list.addItem)
        self.download_thread.finished_downloading_signal.connect(lambda: self.ui.downloaded_list.addItem("Finished Downloading\n"))
        
        self.app.aboutToQuit.connect(lambda: self._save_options(self.default_config_location))
        
    
    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())
        
    def _load_options(self, config_file=None):
        if config_file == None:
            fileName, _ = QFileDialog.getOpenFileName(self.MainWindow,
                                                  "Load Options",
                                                  str(self.user_options_dir),
                                                  "Config Files (*.cfg)", 
                                                  options= QFileDialog.Options())
        else:
            fileName = config_file
            if not fileName.exists():
                return
        
        if fileName:
            config = ConfigParser()
            with open(fileName, 'r') as f:
                config.read_file(f)
                
                checkboxes = config['checkboxes']
                self.ui.archive_checkbox.setChecked(checkboxes.getboolean('use_archive'))
                self.ui.mp3_convert_checkbox.setChecked(checkboxes.getboolean('mp3_convert'))
                self.ui.plist_checkbox.setChecked(checkboxes.getboolean('plist'))
                
                paths = config['paths']
                self.ui.download_folder_input.setText(paths['download_folder'])
                self.ui.plists_file_input.setText(paths['plist_input_file'])
                self.ui.template_input.setText(paths['template'])
                self.ui.ffmpeg_bin_input.setText(paths['ffmpeg_bin'])
                
                self.ui.url_input.setText(config['DEFAULT']['url'])
                
                
    def _save_options(self, config_file=None):
        if config_file == None:
            fileName, _ = QFileDialog.getSaveFileName(self.MainWindow,
                                                  "Save Options",
                                                  str(self.user_options_dir),
                                                  "Config Files (*.cfg)", 
                                                  options= QFileDialog.Options())
        else:
            fileName = config_file
        
        if fileName:
            config = ConfigParser()
            
            config['checkboxes'] = {'use_archive': self.ui.archive_checkbox.isChecked(),
                                            'mp3_convert': self.ui.mp3_convert_checkbox.isChecked(),
                                            'plist': self.ui.plist_checkbox.isChecked()
                                    }
            
            config['paths'] = {'download_folder': self.ui.download_folder_input.text(),
                               'plist_input_file': self.ui.plists_file_input.text(),
                               'template': self.ui.template_input.text().replace('%', '%%'),
                               'ffmpeg_bin': self.ui.ffmpeg_bin_input.text()
                                }
            
            config['DEFAULT'] = {'url': self.ui.url_input.text()}
            
            with open(fileName, 'w') as f:
                config.write(f)

        
    def _progress_hook(self, d): 
        if d['status'] == 'finished'and d.get('filename', False):
            k_bytes = d.get('downloaded_bytes', 0)/1000
            byte_str = "KB" if k_bytes < 1000 else "GB"
            k_bytes = k_bytes if k_bytes < 1000 else k_bytes/1000
            filename = Path(d['filename']).stem
            
            format_string = (
                f"Downloaded: {filename:32.32}{'...' if len(filename) > 32 else '   '}\t"
                f"{k_bytes:4.2f} {byte_str}\t"
                f"{int(d.get('elapsed', 0))//60:02}:{int(d.get('elapsed', 0))%60:02}"
            )
            
            self.download_thread.list_item_string_signal.emit(format_string)
        
        elif d['status'] == 'downloading' and d.get('filename', False):
            filename = f" {Path(d['filename']).stem} "
            eta = f"ETA {d['eta']//60:02}:{d['eta']%60:02}" if d.get('eta', False) else "ETA --:--"
            speed = f"{d['speed']/1000:2.2f} KB/s" if d.get('speed', False) else "---- KB/s"
            percent = int(d['downloaded_bytes']/d['total_bytes']*100) if d.get('downloaded_bytes', False) and d.get('total_bytes', False) else 0
            
            self.download_thread.eta_signal.emit(eta)
            self.download_thread.speed_signal.emit(speed)
            if percent > 0:
                self.download_thread.percent_signal.emit(percent)
            if not self.download_thread.emittedFilename:
                self.download_thread.filename_signal.emit(filename)
                self.download_thread.emittedFilename = True
                    
            
    def _start_download(self):
        url = self.ui.url_input.text()
        options = {
            'verbose': True,
            'noplaylist': True,
            'format': 'best',
            'nooverwrites': True,
            'nopart': True,
            'ignoreerrors': True,
            'continuedl': True,
            # 'logtostderr': True,
            'progress_hooks': [self._progress_hook]
        }
        
        if self.ui.mp3_convert_checkbox.isChecked():
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }, {
                'key': 'FFmpegMetadata'
            }, {
                'key': 'EmbedThumbnail'
            }]
            options['ffmpeg_location'] = self.ui.ffmpeg_bin_input.text()
            options['writethumbnail'] = True
            options['format'] = 'bestaudio/best'
            
        if self.ui.plist_checkbox.isChecked():
            options['noplaylist'] = False
            
        if self.ui.archive_checkbox.isChecked():
            archive_file = "audio_archive.txt" if self.ui.mp3_convert_checkbox.isChecked() else "video_archive.txt"
            archive_file = self.archive_dir / archive_file
            archive_file.touch(exist_ok=True)
            options['download_archive'] = str(archive_file)
        
        if self.ui.download_folder_input.text() == "":
            template = (Path.home() / 'Downloads/').as_posix()
        else:
            template = self.ui.download_folder_input.text() + '/'
            
        if self.ui.template_input.text() != "":
            template = str(Path().home() / 'Downloads') if template == "" else template
            template += self.ui.template_input.text()
        else:
            template += "%(title)s-%(id)s"
        
        options['outtmpl'] = template
            
        if self.ui.plists_file_input.text() != "":
            config = ConfigParser()
            with open(self.ui.plists_file_input.text(), 'r') as f:
                config.read_file(f)
                for playlist_name in config.sections():
                    playlist = config[playlist_name]
                    options['playliststart'] = playlist.getint('start')
                    options['playlistend'] = playlist.getint('end')
                    options['noplaylist'] = False
                    url = playlist['url']
        
        print(f"{options =}")
        
        self.download_thread.wait()
        self.download_thread.fill(url, options)
        self.download_thread.start()
        self.download_thread.setPriority(QThread.HighestPriority)
        
        

def main(start_config=None, log_file=None):
    if log_file != None:
        sys.stdout = open(log_file, "a")
        x = datetime.datetime.now()
        print(f"\n\nRun:\t{x.year}/{x.month}/{x.day}  {x.hour:02}:{x.minute:02}:{x.second:02}\n")
        
    contr = Ui_Controller(start_config)
    contr.start()
    
if __name__ == "__main__":
    main()
    
