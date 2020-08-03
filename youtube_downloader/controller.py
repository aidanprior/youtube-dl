import sys
import youtube_dl
import winshell

from pathlib import Path
from configparser import ConfigParser

from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from PyQt5.QtCore import QDir, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from .ui import Ui_MainWindow
from .update import update_youtube_dl, update_this


class Download_Thread(QThread):

    eta_signal = pyqtSignal(str)
    speed_signal = pyqtSignal(str)
    percent_signal = pyqtSignal(int)
    filename_signal = pyqtSignal(str)
    list_item_string_signal = pyqtSignal(str)
    finished_downloading_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Download_Thread, self).__init__(parent=parent)

    def fill(self, url, options):
        self.url = url
        self.options = options

    def run(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            output = ydl.download([self.url])
            self.finished_downloading_signal.emit(output)
            return


class Ui_Controller():
    def __init__(self, start_config=None):
        self._create_dirs()
        self.options_list = []
        self.urls = []
        self.plist_names = []

        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.MainWindow.setWindowIcon(QIcon("icon.ico"))
        self.ui = Ui_MainWindow()

        self.download_thread = Download_Thread()

        self.ui.setupUi(self.MainWindow)
        self._setup_connections()

        if start_config is None:
            self._load_options(self.default_config_location)
        elif start_config == "EMPTY":
            pass
        elif not (self.user_options_dir / start_config).exists():
            raise Exception(f"Passed Config File Path doesn't\
                 exist! ({self.user_options_dir / start_config})")
        else:
            self._load_options(self.user_options_dir / start_config)

    def _create_dirs(self):
        def full_path_create(p):
            tmp = p.parent
            while not tmp.exists():
                tmp.mkdir()
                tmp = tmp.parent

        self.data_dir = Path(winshell.application_data()) / \
            'Youtube Downloader'
        self.archive_dir = self.data_dir / 'archives'
        self.user_options_dir = self.data_dir / 'User Options'
        self.plist_inputs_dir = self.data_dir / 'Multi-Playlist Configs'
        self.default_config_location = self.data_dir / \
            "last_opened_options.cfg"

        full_path_create(self.data_dir)
        full_path_create(self.archive_dir)
        full_path_create(self.user_options_dir)
        full_path_create(self.plist_inputs_dir)

    def _setup_connections(self):
        def get_download_folder():
            self.ui.download_folder_input.setText(
                QFileDialog.getExistingDirectory(self.MainWindow,
                                                 "Set Download Folder",
                                                 (Path.home()/'Downloads')
                                                 .as_posix()))
        self.ui.download_folder_browse_button.clicked.connect(
            get_download_folder)

        def get_ffmpeg_bin():
            self.ui.ffmpeg_bin_input.setText(
                QFileDialog.getExistingDirectory(self.MainWindow,
                                                 "Set FFmpeg Bin",
                                                 QDir.rootPath()))
        self.ui.ffmpeg_bin_browse_button.clicked.connect(get_ffmpeg_bin)

        def get_plists_file():
            self.ui.plists_file_input.setText(
                QFileDialog.getOpenFileName(self.MainWindow,
                                            "Load Multi-Playlist Config",
                                            str(self.plist_inputs_dir),
                                            "Config Files (*.cfg)",
                                            options=QFileDialog.Options())[0])
        self.ui.plists_file_browse_button.clicked.connect(get_plists_file)

        self.ui.load_options_button.clicked.connect(
            lambda: self._load_options())
        self.ui.save_options_button.clicked.connect(
            lambda: self._save_options())

        self.ui.download_now_button.clicked.connect(self._create_download)

        self.ui.update_button.clicked.connect(update_this)

        self.ui.ytdl_update_button.clicked.connect(update_youtube_dl)

        self.download_thread.eta_signal.connect(
            self.ui.eta_label.setText)
        self.download_thread.speed_signal.connect(
            self.ui.speed_label.setText)
        self.download_thread.percent_signal.connect(
            self.ui.download_progressbar.setValue)
        self.download_thread.filename_signal.connect(
            self.ui.download_filename_label.setText)
        self.download_thread.list_item_string_signal.connect(
            self.ui.downloaded_list.addItem)

        def finish_downloading():
            self.ui.download_filename_label.setText("Finished")
            self.ui.downloaded_list.addItem("Finished Downloading")
            self._download()

        self.download_thread.finished_downloading_signal\
            .connect(finish_downloading)

        self.app.aboutToQuit.connect(self._exit)

    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def _load_options(self, config_file=None):
        if config_file is None:
            fileName, _ = QFileDialog\
                .getOpenFileName(self.MainWindow,
                                 "Load Options",
                                 str(self.user_options_dir),
                                 "Config Files (*.cfg)",
                                 options=QFileDialog.Options())
        else:
            fileName = config_file
            if not fileName.exists():
                return

        if fileName:
            config = ConfigParser()
            with open(fileName, 'r') as f:
                config.read_file(f)

                checkboxes = config['checkboxes']
                self.ui.archive_checkbox.setChecked(
                    checkboxes.getboolean('use_archive'))
                self.ui.mp3_convert_checkbox.setChecked(
                    checkboxes.getboolean('mp3_convert'))
                self.ui.plist_checkbox.setChecked(
                    checkboxes.getboolean('plist'))

                paths = config['paths']
                self.ui.download_folder_input.setText(paths['download_folder'])
                self.ui.plists_file_input.setText(paths['plist_input_file'])
                self.ui.template_input.setText(paths['template'])
                self.ui.ffmpeg_bin_input.setText(paths['ffmpeg_bin'])

                self.ui.url_input.setText(config['DEFAULT']['url'])
                self.MainWindow.resize(config['DEFAULT'].getint('width'),
                                       config['DEFAULT'].getint('height'))

    def _save_options(self, config_file=None):
        if config_file is None:
            fileName, _ = QFileDialog\
                .getSaveFileName(self.MainWindow,
                                 "Save Options",
                                 str(self.user_options_dir),
                                 "Config Files (*.cfg)",
                                 options=QFileDialog.Options())
        else:
            fileName = config_file

        if fileName:
            config = ConfigParser()

            config['checkboxes'] = {'use_archive':
                                    self.ui.archive_checkbox.isChecked(),
                                    'mp3_convert':
                                    self.ui.mp3_convert_checkbox.isChecked(),
                                    'plist': self.ui.plist_checkbox.isChecked()
                                    }

            config['paths'] = {'download_folder':
                               self.ui.download_folder_input.text(),
                               'plist_input_file':
                               self.ui.plists_file_input.text(),
                               'template':
                               self.ui.template_input.text().replace('%',
                                                                     '%%'),
                               'ffmpeg_bin': self.ui.ffmpeg_bin_input.text()
                               }

            size = self.MainWindow.size()
            config['DEFAULT'] = {'url': self.ui.url_input.text(),
                                 'width': size.width(),
                                 'height': size.height()
                                 }

            with open(fileName, 'w') as f:
                config.write(f)

    def _progress_hook(self, d):
        if d['status'] == 'finished' and d.get('filename', False):
            k_bytes = d.get('downloaded_bytes', 0)/1000

            if k_bytes == 0:
                return

            byte_str = "KB" if k_bytes < 1000 else "GB"
            k_bytes = k_bytes if k_bytes < 1000 else k_bytes/1000
            filename = Path(d['filename']).stem

            format_string = (
                f"\tDownloaded: {filename:32.32}"
                f"{'...' if len(filename) > 32 else '   '}    "
                f"{k_bytes:4.2f} {byte_str}    "
                f"{int(d.get('elapsed', 0))//60:02}:"
                f"{int(d.get('elapsed', 0))%60:02}"
            )
            self.download_thread.list_item_string_signal.emit(format_string)
            self.download_thread.filename_signal.emit(
                f"Post Processing : {filename}")
            self.download_thread.eta_signal.emit("ETA --:--")
            self.download_thread.speed_signal.emit(" 0.00 KB/s")
            self.download_thread.percent_signal.emit(0)

        elif d['status'] == 'downloading' and d.get('filename', False):
            filename = f" {Path(d['filename']).stem} "
            eta = f"ETA {d['eta']//60:02}:{d['eta']%60:02}" if\
                d.get('eta', False) else "ETA --:--"
            speed = f"{d['speed']/1000:2.2f} KB/s" if d.get('speed', False)\
                else "---- KB/s"
            percent = int(d['downloaded_bytes']/d['total_bytes']*100)\
                if d.get('downloaded_bytes', False)\
                and d.get('total_bytes', False) else 0

            self.download_thread.eta_signal.emit(eta)
            self.download_thread.speed_signal.emit(speed)
            if percent > 0:
                self.download_thread.percent_signal.emit(percent)
            self.download_thread.filename_signal.emit(filename)

    def _exit(self):
        self._save_options(self.default_config_location)

    def _create_download(self):
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
            options['ffmpeg_location'] = str(
                Path(self.ui.ffmpeg_bin_input.text()))
            options['writethumbnail'] = True
            options['format'] = 'bestaudio/best'

        if self.ui.plist_checkbox.isChecked():
            options['noplaylist'] = False
            plist_name = ""
        else:
            plist_name = None

        if self.ui.archive_checkbox.isChecked():
            archive_file = "audio_archive.txt" if self.ui.mp3_convert_checkbox\
                .isChecked() else "video_archive.txt"
            archive_file = self.archive_dir / archive_file
            archive_file.touch(exist_ok=True)
            options['download_archive'] = str(archive_file)

        if self.ui.download_folder_input.text() == "":
            template = (Path.home() / 'Downloads/').as_posix()
        else:
            template = self.ui.download_folder_input.text() + '/'

        if self.ui.template_input.text() != "":
            template = str(Path().home() / 'Downloads') if template == "" \
                else template
            template += self.ui.template_input.text()
        else:
            template += "%(title)s-%(id)s"

        options['outtmpl'] = template

        if self.ui.plists_file_input.text() != "":
            config = ConfigParser()
            with open(self.ui.plists_file_input.text(), 'r') as f:
                config.read_file(f)
                for playlist_name in config.sections():
                    options_temp = options.copy()
                    playlist = config[playlist_name]
                    options_temp['playliststart'] = playlist.getint('start')
                    options_temp['playlistend'] = playlist.getint('end')
                    options_temp['noplaylist'] = False

                    self.urls.append(playlist['url'])
                    self.options_list.append(options_temp)
                    self.plist_names.append(playlist_name)

        else:
            self.urls.append(url)
            self.options_list.append(options)
            self.plist_names.append(plist_name)

        self._download()

    def _download(self):
        if len(self.urls) == 0:
            return

        if self.plist_names[-1] is not None:
            self.ui.downloaded_list.addItem(f"Downloading from playlist \
                {self.plist_names[-1]}")

        print(f"{self.options_list[-1] = }")
        self.download_thread.fill(self.urls[-1], self.options_list[-1])
        self.urls = self.urls[:-1]
        self.options_list = self.options_list[:-1]
        self.plist_names = self.plist_names[:-1]
        self.download_thread.start()
        self.download_thread.setPriority(QThread.HighestPriority)


def main(start_config=None):
    contr = Ui_Controller(start_config)
    contr.start()


if __name__ == "__main__":
    main()
