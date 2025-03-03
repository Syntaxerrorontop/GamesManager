from . import os, subprocess, logging

from .commen import Folder, CACHE_DIR, VIDEO_DIR, TOOLS_DIR, TEMP_DIR
class Player:
    def __init__(self):
        Folder.check_existence(os.getcwd(), CACHE_DIR, create = True)
        Folder.check_existence(os.getcwd(), VIDEO_DIR, create = True)

        self.ffplay_path = os.path.join(os.getcwd(), TOOLS_DIR, "ffplay.exe")
    
    def update(self):
        pass
    
    def play(self, video_path, last_paused_string = ""):
        logging.info(f"Playing video: {video_path}")
        command = [self.ffplay_path, video_path]
        
        logging.info(f"command: {command}")
        
        Folder.check_existence(os.getcwd(), TEMP_DIR, create = True)
        
        name = os.path.basename(video_path)
        
        length = len(name.split("."))
        
        txt_name = name[:length - 1]
        
        if last_paused_string:
            command += ["-ss", last_paused_string] + [">", os.path.join(os.getcwd(), TEMP_DIR, f"{txt_name}.txt")]
            
        process = subprocess.Popen(command)
        
        process.wait()
        
        