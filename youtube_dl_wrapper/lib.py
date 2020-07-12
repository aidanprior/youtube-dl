import logging
from pathlib import Path
from configparser import ConfigParser

total_downloaded = 0

HOME = Path.home()
THIS_DIR = Path(__file__).parent
CONFIG_FILE = THIS_DIR / "config.ini"

def get_config(config_section):
    config = ConfigParser(allow_no_value=False)
    
    with open(CONFIG_FILE, "r+") as f:
        config.read_file(f) 
        
        if config['DEFAULT']['home_dir'] == "":
            config['DEFAULT']['home_dir'] = HOME.as_posix()
            
        if config['DEFAULT']['this_dir'] == "":
            config['DEFAULT']['this_dir'] = THIS_DIR.as_posix()      
        
    with open(CONFIG_FILE, "w+") as f:
        config.write(f)
    
    return dict(config.items(config_section))
    


def setup_loggers(config_section):
    log_file = Path(get_config(config_section)['log'])
    
    c_handler = logging.StreamHandler()
    c_format = logging.Formatter('%(filename)s : %(lineno)d - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    c_handler.setLevel(logging.CRITICAL)

    f_handler = logging.FileHandler(log_file)
    f_format = logging.Formatter('%(asctime)s - %(filename)s : %(lineno)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    f_handler.setFormatter(f_format)
    f_handler.setLevel(logging.DEBUG)

    lgr = logging.getLogger(__name__)
    lgr.addHandler(c_handler)
    lgr.addHandler(f_handler)
    
    return lgr

def create_hook(input_byte_level):    
    def progress_hook(d):
        global total_downloaded
        byte_level = input_byte_level
        byte_divisors = {'kB': 1024, 'mB': 1024**2, 'gB': 1024**3}
        byte_divisor = byte_divisors[byte_level]
        
        if d['status'] == 'finished'and d.get('filename', False):
            format_string = (
                f"Downloaded: {Path(d['filename']).stem:32.32}    "
                f"{d.get('downloaded_bytes', -1)/byte_divisor:4.2f}{byte_level}    "
                f"in    {int(d.get('elapsed', 0))//60:02}:{int(d.get('elapsed', 0))%60:02}"
            )
            
            print()
            print(format_string)
            total_downloaded += 1
        
        elif d['status'] == 'downloading' and d.get('filename', False):
            format_string = (
                f"{Path(d['filename']).stem:32.32} "
                f"{int(d.get('speed', 0)/1024):5}kB/s "
                f"{int(d.get('downloaded_bytes', 0)/d.get('total_bytes', 1)*100)}% "
                f"ETA {d.get('eta', 0)//60:02}:{d.get('eta', 0)%60:02}"
            )
            
            print(" " * len('Downloaded: ') + f"{format_string}\r", end="")
            
    return progress_hook

