from . import time, subprocess, os, psutil, logging, json
from .commen import CONFIG_DIR, GAMES_JSON_DATA, save_json, load_json

class GameInstance:
    def __init__(self, name, path, args, play_button):
        self.game_name = name
        self.executable_path = path
        self._start_time: float = 0
        self.args = args
        
        self.__process = None
        
        self.qt_play_button = play_button
    
    def _start_playtime(self):
        self._start_time = time.time()
    
    def start(self):
        if self.__process:
            self.close()
            self.qt_play_button.setText("Play")
            return None
        
        self.qt_play_button.setText("Stop")
        print(self.executable_path)
        self._start_playtime()
        run_data = [self.executable_path] + self.args
        self.__process = subprocess.Popen(run_data)
    
    def wait(self):
        try:
            self.__process.wait()
        except AttributeError:
            pass
        played_time = time.time() - self._start_time
        self.update_playtime(played_time)
    
    def close(self):
            #self.__process.kill()
        try:
            parent = psutil.Process(self.__process.pid)
            
            for child in parent.children(recursive=True):
                child.terminate()
            
            parent.terminate()
            parent.wait(timeout=5)
            
            if parent.is_running():
                parent.kill()
            self.__process = None
        except psutil.NoSuchProcess:
            self.__process = None
            self.start()
    
    def update_playtime(self, playtime: float):
        try:
            data = load_json(os.path.join(os.getcwd(), CONFIG_DIR, GAMES_JSON_DATA))
            data["Games"][self.game_name]["playtime"] = int(float(data["Games"][self.game_name]["playtime"]) + float(playtime))
            #print(data)
            save_json(os.path.join(os.getcwd(), CONFIG_DIR, GAMES_JSON_DATA), data)
        except json.JSONDecodeError as e:
            logging.warning(f"Error while saving Playtime: {e}")