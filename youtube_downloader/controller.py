import sys
import youtube_dl
from pathlib import Path
from configparser import ConfigParser
from contextlib import redirect_stdout
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

from ui import Ui_MainWindow


class ui_controller():
    def __init__(self):
        self._create_dirs()
        
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.config = ConfigParser()
        
        self.ui.setupUi(self.MainWindow)
        self._setup_connections()
        
    
    def _create_dirs(self):
        self.data_dir = Path(__file__).parent / 'data'
        self.user_options_dir = self.data_dir / 'User Options'
        self.plist_inputs_dir = self.data_dir / 'Multi-Playlist Configs'
        
        self.data_dir.mkdir(exist_ok=True)
        self.user_options_dir.mkdir(exist_ok=True)
        self.plist_inputs_dir.mkdir(exist_ok=True)
    
    
    def _setup_connections(self):
        get_download_folder = lambda: self.ui.download_folder_input.setText(self._pick_folder(str(Path().home())))
        self.ui.download_folder_browse_button.clicked.connect(get_download_folder)
        
        get_ffmpeg_bin = lambda: self.ui.ffmpeg_bin_input.setText(self._pick_folder(str(Path().home())))
        self.ui.ffmpeg_bin_browse_button.clicked.connect(get_ffmpeg_bin)
        
        get_plists_file = lambda: self.ui.plists_file_input.setText(self._pick_file(str(self.user_options_dir)))
        self.ui.plists_file_browse_button.clicked.connect(get_plists_file)
        
        self.ui.load_options_button.clicked.connect(self._load_options)
        self.ui.save_options_button.clicked.connect(self._save_options)
        
        self.ui.download_now_button.clicked.connect(self._start_download)
        
    
    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())
        
    def _load_options(self):
        load_dialog = QFileDialog()
        load_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        load_dialog.setFileMode(QFileDialog.ExistingFile)
        load_dialog.setViewMode(QFileDialog.List)
        load_dialog.setFilter("Config files (*.cfg)")
        load_dialog.setDirectory(str(self.user_options_dir))
        
        if load_dialog.exec_():
            filename = load_dialog.selectedFiles()[0]
            with open(filename, 'r') as f:
                self.config.read_file(f)
                
                checkboxes = self.config['checkboxes']
                self.ui.archive_checkbox.setChecked(checkboxes.getboolean('use_archive'))
                self.ui.mp3_convert_checkbox.setChecked(checkboxes.getboolean('mp3_convert'))
                self.ui.plist_checkbox.setChecked(checkboxes.getboolean('plist'))
                
                paths = self.config['paths']
                self.ui.download_folder_input.setText(paths['download_folder'])
                self.ui.plists_file_input.setText(paths['plist_input_file'])
                self.ui.template_input.setText(paths['template'])
                
                self.ui.url_input.setText(self.config['DEFAULT']['id'])
                
                
    def _save_options(self):
        save_dialog = QFileDialog()
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setFileMode(QFileDialog.AnyFile)
        save_dialog.setViewMode(QFileDialog.List)
        # save_dialog.setFilter("Text files (*.cfg)")
        save_dialog.setDirectory(str(self.user_options_dir))
        
        if save_dialog.exec_():
            filename = save_dialog.selectedFiles()[0]
            with open(filename, 'w') as f:
                self.config.read_file(f)
                
                checkboxes = self.config['checkboxes']
                checkboxes['use_archive'] = self.ui.archive_checkbox.isChecked()
                checkboxes['mp3_convert'] = self.ui.mp3_convert_checkbox.isChecked()
                checkboxes['plist'] = self.ui.plist_checkbox.isChecked()
                
                paths = self.config['paths']
                paths['download_folder'] = self.ui.download_folder_input.text()
                paths['plist_input_file'] = self.ui.plists_file_input.text()
                paths['template'] = self.ui.template_input.text()
                
                self.config['DEFAULT']['url'] = self.ui.url_input.text()
                
                
    def _pick_folder(self, start_dir):
        load_dialog = QFileDialog()
        load_dialog.setFileMode(QFileDialog.Directory)
        load_dialog.setOption(QFileDialog.ShowDirsOnly)
        load_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        load_dialog.setViewMode(QFileDialog.List)
        load_dialog.setDirectory(start_dir)
                                 
        if load_dialog.exec_():
            return load_dialog.selectedFiles()[0]
            
            
    def _pick_file(self, start_dir):
        load_dialog = QFileDialog()
        load_dialog.setFileMode(QFileDialog.ExistingFile)
        load_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        load_dialog.setViewMode(QFileDialog.List)
        load_dialog.setFilter("Config files (*.cfg)")
        load_dialog.setDirectory(start_dir)
                                 
        if load_dialog.exec_():
            return load_dialog.selectedFiles()[0]
        
    def _progress_hook(self, d):        
        if d['status'] == 'finished'and d.get('filename', False):
            k_bytes = d.get('downloaded_bytes', 0)/1024
            byte_str = "kB" if k_bytes < 1024 else "gB"
            k_bytes = k_bytes if k_bytes < 1024 else k_bytes/1024
            
            format_string = (
                f"Downloaded: {Path(d['filename']).stem:32.32} "
                f"{k_bytes:4.2f} {byte_str} "
                f"in {int(d.get('elapsed', 0))//60:02}:{int(d.get('elapsed', 0))%60:02}"
            )
            
            self.ui.downloaded_list.addItem(format_string)
        
        elif d['status'] == 'downloading' and d.get('filename', False):
            filename = f" {Path(d['filename']).stem} "
            eta = f"ETA {d.get('eta', 0)//60:02}:{d.get('eta', 0)%60:02}"
            speed = f"{d.get('speed')/1024:2.2} kB/s"
            percent = int(d.get('downloaded_bytes', 0)/d.get('total_bytes', 1)*100)
            
            self.ui.download_filename_label.setText(filename)
            self.ui.eta_label.setText(eta)
            self.ui.speed_label.setText(speed)
            self.ui.download_progressbar.setValue(percent)
                    
            
    def _start_download(self):
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
            archive_file = self.data_dir / "archives" / archive_file
            options['download_archive'] = str(archive_file)
            
        if self.ui.template_input.text() != "":
            template = self.ui.download_folder_input.text()
            template = str(Path().home() / 'Downloads') if template == "" else template
            template += self.ui.template_input.text()
            options['outtmpl'] = template
            
        if self.ui.plists_file_input.text() != "":
            with open(self.ui.plists_file_input.text(), 'r') as f:
                self.config.read_file(f)
                for playlist_name in self.config.sections():
                    playlist = self.config[playlist_name]
                    options['playliststart'] = playlist.getint('start')
                    options['playlistend'] = playlist.getint('end')
                    options['noplaylist'] = False
                    url = playlist['url']
                
                    self._download(url, options)
        else:
            self._download(self.ui.url_input.text(), options)
            
        
    def _download(self, url, options):
        with open('data/youtube-dl.log', 'a+') as f:
            with redirect_stdout(f):
                print('\n\nSTARTING YOUTUBE-DL...\n\n')
                with youtube_dl.YoutubeDL(options) as ydl:
                    ydl.download(url)
        

def main():
    controller = ui_controller()
    controller.start()
    
if __name__ == "__main__":
    main()
    
