################################################
# Imports

from . import logging, os, shutil, json, ctypes

from .Plugins.PluginManager import PluginManager

###############################################
# Inits

logging.basicConfig(level=logging.DEBUG)

################################################
# Function/Classes for Vars

class File:
    @staticmethod
    def check_existence(in_path, file_name, create = True, add_conten = "", use_json = False) -> bool:
        logging.info(f"Checking {file_name} existence in {in_path}.")

        if not file_name in os.listdir(in_path):
            logging.info(f"File not found")
            with open(os.path.join(in_path, file_name), "w") as file:
                file.close()
                logging.info(f"File created: {create} {file_name}")
                
                if add_conten != "":
                    with open(os.path.join(in_path, file_name), "w") as file:
                        if use_json:
                            json.dump(add_conten, file, indent=4)
                        else:
                            file.write(add_conten)
                        file.close()
                    logging.info(f"Added content to {file_name}")
                
                return True
            
            return False
        
        logging.info("File already exists")
        
        return True

class Cords:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y
    
    def get(self):
        logging.debug(f"Cord: ({self.x} | {self.y})")
        return (self.x, self.y)

def save_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
        file.close()

def load_json(path) -> dict:
    with open(path, "r") as file:
        __data = json.load(file)
        file.close()
    
    return __data


def get_QSS(path) -> str:
    logging.info(f"Asset_Manager: Loading: '{path}'")
    with open(path, "r") as file:
        qss = str(file.read())
        file.close()
    
    return qss

def get_file_content(in_path, filename, error_data = "") -> str:
    File.check_existence(in_path, filename, create=True, add_conten=error_data)
    
    with open(os.path.join(in_path, filename), "r") as file:
        data = file.read()
        file.close()
    
    return data

def _gen_config_path(config_file_name) -> str:
    if config_file_name != "":
        logging.debug(f"Config_path: {config_file_name}")
        return os.path.join(os.getcwd(), CONFIG_DIR, config_file_name)
    else:
        logging.debug(f"Config_path: {CONFIG_DIR}")
        return os.path.join(os.getcwd(), CONFIG_DIR)

def _gen_asset_path(name) -> str:
    logging.debug(f"Asset_path: {name}")
    return os.path.join(os.getcwd(), ASSET_DIR, name)

################################################
# User Changable Vars



################################################
# DEFAULT CONST

class AssetFilenames:
    tabbutton_stylsheet = "tabbutton.QSS"
    tabwidget_sylesheet = "tabwidget.QSS"
    gamename_stylesheet = "gamename.QSS"
    playtime_stylesheet = "playtime.QSS"
    play_button_stylsheet = "playbutton.QSS"
    main_stylesheet = "mainstylesheet.QSS"
    libary_stacked_widget_button = "libarystackedwidgetbutton.QSS"
    default_background_color = "default_background.QSS"
    game_scrollable_area_libary = "gamesbrowser.QSS"
    qline_edit_args_libary = "argslineedit.QSS"
    args_save_button_libary = "argssavebutton.QSS"

class UserConfig:
    def __init__(self, in_path, filename):
        File.check_existence(in_path, filename, add_conten={"install_commen_redist": True, "shutil_move_error_replace": True, "search": {"games": True, "movies": False, "series": False}}, use_json=True)
        self._path = os.path.join(in_path, filename)
        self._data = load_json(self._path)
        
        self.SHUTIL_MOVE_ERROR_REPLACE = self._data["shutil_move_error_replace"]
        self.INSTALL_COMMENREDIST_STEAMRIP = self._data["install_commen_redist"]
        
        self.SEARCH_GAMES = self._data["search"]["games"]
        self.SEARCH_MOVIES = self._data["search"]["movies"]
        self.SEARCH_SERIES = self._data["search"]["series"]
    

GAME_DIR = "Games"
CONFIG_DIR = "Config"
TEMP_DIR = "Temp"
TOOLS_DIR = "Tools"
ASSET_DIR = "Assets"
CACHE_DIR = "Cache"
VIDEO_DIR = "Videos"

GAMES_JSON_DATA = "games.json"
STEAMRIP_JSON_NAME = "steamrip.json"
USER_CONFIG_JSON_NAME = "userconfig.json"

NAME = "SyntaxRipper"
DOWNLOADER_VERSION = "1.0.0"

HEADLESS = False

################################################
# Consts using function

PLUGIN_MANAGER = PluginManager()

WINDOW_SIZE = Cords(1920, 1080)

USER_CONFIG = UserConfig(_gen_config_path(""), USER_CONFIG_JSON_NAME)

TAB_BUTTON_STYLESHEET = get_QSS(_gen_asset_path(AssetFilenames.tabbutton_stylsheet))
TAB_QWIDGET_STYLESHEET = get_QSS(_gen_asset_path(AssetFilenames.tabwidget_sylesheet))
GAME_NAME_STYLESHEET_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.gamename_stylesheet))
GAME_PLAYTIME_STYLESHEET_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.playtime_stylesheet))
PLAY_BUTTON_STYLESHEET_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.play_button_stylsheet))
MAIN_STYLESHEET = get_QSS(_gen_asset_path(AssetFilenames.main_stylesheet))
STACKED_WIDGET_BUTTON_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.libary_stacked_widget_button))
DEFAULT_BACKGROUND_COLOR = get_QSS(_gen_asset_path(AssetFilenames.default_background_color))
GAMES_BROWSER_SCROLLABLE_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.game_scrollable_area_libary))
QLINE_EDIT_ARGS_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.qline_edit_args_libary))
ARGS_SAVE_BUTTON_LIBARY = get_QSS(_gen_asset_path(AssetFilenames.args_save_button_libary))

VERSION = get_file_content(os.path.join(os.getcwd(), CONFIG_DIR), "version.txt", error_data="0.1.2")

################################################
# Consts 

DYNAMIC_SEARCH_NAME = "dynamic_search"


################################################
# Const Using other Consts

WINDOW_TITLE = f"{NAME}_{VERSION}"

###############################################
# error codes

error = {
    -1: "1Ficher on cooldown"
}

class Folder:
    @staticmethod
    def move(folder_path_to_move, move_in_folder):
        logging.info(f"Moving {folder_path_to_move} to {move_in_folder}")
        try:
            shutil.move(folder_path_to_move, move_in_folder)
        
        except shutil.Error as e:
            logging.error(f"Moving the file encountered a error: {e}")
            logging.info(f"Delete folder and replace with new: {USER_CONFIG.SHUTIL_MOVE_ERROR_REPLACE}")
            
            if USER_CONFIG.SHUTIL_MOVE_ERROR_REPLACE:
                shutil.rmtree(os.path.join(move_in_folder,os.path.basename(os.path.normpath(folder_path_to_move))))
                logging.info("Deleted old Installation, applaying new patch")
                shutil.move(folder_path_to_move, move_in_folder)
    
    @staticmethod
    def delete(folder_path):
        logging.info(f"Deleting: {folder_path}")
        shutil.rmtree(folder_path)
    
    def check_existence(in_path, folder_name, create = True) -> bool:
        logging.info(f"Checking {folder_name} existence in {in_path}.")

        if not folder_name in os.listdir(in_path):
            logging.info(f"folder not detected creating: {create}")
            
            if create:
                os.mkdir(os.path.join(in_path, folder_name))
                return True
            
            return False
        
        logging.info("Folder already exists")
        
        return True

class Payload:
    def __init__(self):
        logging.debug("Payload created")
        self._payload = {}
    
    def add_operation(self, operation):
        logging.debug(f"PAYLOAD: operation added: {operation}")
        self._payload["op"] = operation
    
    def add_id(self, id):
        logging.debug(f"PAYLOAD: id added: {id}")
        self._payload["id"] = id
    
    def add_rand(self, rand):
        logging.debug(f"PAYLOAD: rand added: {rand}")
        self._payload["rand"] = rand
    
    def add_referer(self, referer):
        logging.debug(f"PAYLOAD: referer added: {referer}")
        self._payload["referer"] = referer
    
    def add_method_free(self, method):
        logging.debug(f"PAYLOAD: free_method added: {method}")
        self._payload["method_free"] = method
    
    def add_method_premium(self, method):
        logging.debug(f"PAYLOAD: premium_method added: {method}")
        self._payload["method_premium"] = method
    
    def add_dl(self, dl):
        logging.debug(f"PAYLOAD: dl added: {dl}")
        self._payload["dl"] = dl
    
    def get(self):
        logging.debug(f"Payload generated: {self._payload}")
        return self._payload

class Header:
    def __init__(self):
        self._headers = {}
    
    def add_user_agent(self, user_agent):
        self._headers['user-agent'] = user_agent
    
    def add_authority(self, authority):
        self._headers['authority'] = authority
    
    def add_method(self, method):
        self._headers['method'] = method
    
    def add_path(self, path):
        self._headers["path"] = path
    
    def add_referer(self, referer):
        self._headers['referer'] = referer
    
    def add_hx_request(self, hx_request):
        self._headers['hx_request'] = hx_request
    
    def add_others(self, key, value):
        self._headers[key] = value
    
    def get_headers(self):
        return self._headers

def ask_yes_no(question):
    result = ctypes.windll.user32.MessageBoxW(0, question, "Confirmation", 4)
    return result == 6  # 6 = IDYES, 7 = IDNO

# Generating every Possible needed folder
Folder.check_existence(os.getcwd(), CONFIG_DIR)
Folder.check_existence(os.getcwd(), GAME_DIR)

File.check_existence(os.path.join(os.getcwd(), CONFIG_DIR), GAMES_JSON_DATA, add_conten={"Games": {}}, use_json=True)
File.check_existence(os.path.join(os.getcwd(), CONFIG_DIR), STEAMRIP_JSON_NAME, add_conten={"commenredist": []}, use_json=True)