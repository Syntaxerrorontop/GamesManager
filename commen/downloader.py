from . import re, time, json, random, string, os, logging
from . import requests, rarfile, tqdm, sync_playwright

from .commen import Header, Payload, Folder, File, load_json, save_json

################################################
# USER config

SHUTIL_MOVE_ERROR_REPLACE = True
INSTALL_COMMENREDIST_STEAMRIP = True

################################################
# DEFAULT CONST

GAME_DIR = "Games"
CONFIG_DIR = "Config"
TEMP_DIR = "Temp"
TOOLS_DIR = "Tools"


GAMES_JSON_DATA = "games.json"
STEAMRIP_JSON_NAME = "steamrip.json"


################################################

def init():
    logging.info("Initiating Dwonloader")
    
    rarfile.UNRAR_TOOL = os.path.join(os.getcwd(), TOOLS_DIR, "UnRAR.exe")

class DirectLinkDownloader:
    @staticmethod
    def megadb(url) -> str:
        print(url)
        _id = url.split("/")[-1]
        return None
    
    @staticmethod
    def filecrypt(url) -> str:
        print(url)
        return None
    
    @staticmethod
    def buzzheavier(url) -> str:
        return {"url": url.replace(r"/f/", r"/") + "/download", "payload": None, "headers": None , "method": "get"}
    
    @staticmethod
    def ficher(url) -> str:
        logging.info("Downloader:1Ficher Using Ficher this can take up to 3 Minutes")
        steps = ["#cmpwelcomebtnyes > a", "#cookie_box > a.cookie_box_close", "#dlb"]
        
        with sync_playwright() as p:
            logging.info("Downloader:1Ficher Creating Broswser intance")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            #stealth_sync(context)  # Apply stealth mode directly
            page = context.new_page()
            logging.info("Downloader:1Ficher Successfull")
            
            page.goto(url)
            
            logging.info("Downloader:1Ficher Site loading finished")
                
            if page.locator("#closeButton").count() > 0:
                    time.sleep(6)
                    page.click("#closeButton")

            for step in steps:

                start_time = time.time()  # Record the start time
                
                page.wait_for_selector(step, timeout=100000)
                page.click(step)                
                
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                
                logging.info(f"Downloader:1Ficher EXECUTED: {step} in {elapsed_time:.2f} seconds")
            
            page.wait_for_selector("body > div.alc > div:nth-child(6) > a", timeout=5000)
            
            link = page.locator("body > div.alc > div:nth-child(6) > a").get_attribute("href")
            
            page.close()
            
            browser.close()
        
        return {"url": link, "payload": None, "headers": None, "method": "get"}

    @staticmethod
    def datanode(url) -> str:
        ids = str(url).split("/")
        for index, id in enumerate(ids):
            if id == "datanodes.to":
                _id = ids[index+1]
                break
        
        headers = Header()
        headers.add_authority("datanodes.to")
        headers.add_method("POST")
        headers.add_hx_request("False")
        headers.add_path("/download")
        headers.add_referer("https://datanodes.to/download")
        headers.add_others("cookie", "lang=german; file_name=God-O-War-Ragnarok-SteamRIP.com.rar; file_code=guziknumxest; affiliate=dOtuOv3qRKAJ2fSUcUnMpzIdz6ueYkMmoXNiCfaBgZWSeYRZgi3SARRHh2jIQ8coMyT8QyluHsyloNJvM84bZAwuxsPtWbSQvkEtNJ2Q4PjOfEWpHkrD5ligTtBuVmWGIfRg; cf_clearance=ImOIuyght4VddGN1jz0xhgwguDk.8on7NtNs1WRyWOc-1737588193-1.2.1.1-Vxe_QzcgRNO3EvCAXYXDqtXZGPcLrWiPDHq5B86FMAX0bZrYs.nhOVNsNXdjHcL3n_Ce47.gWtmTAO8iYg94fuR5k.dO8KWKNtYAN3om7cgQncdgCI3qoap6EBJgRJU1HKT9AWB8yUg6vPGGB3GFGzpv98IEWIQbMF9UYU.4ndMBarRfZkr7vfl816ic4A16.d.1fe_.92OALnmsUZlFv4ut0MLcffjfq9mcDD60_2aGwD_1zOYg0sa4qZizjgZwK11vS7FJm4ro3t4VFy7AxB70XqYkt3sn800PiOKw9U0")
        headers.add_user_agent("Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36")
        
        payload = Payload()
        payload.add_dl("1")
        payload.add_id(_id)
        payload.add_method_free("Kostenloser Download >>")
        payload.add_method_premium("")
        payload.add_operation("download2")
        payload.add_referer("https://datanodes.to/download")
        payload.add_rand("")
        
        logging.info(f"Getting Direct download link with request: https://datanodes.to/download | Payload: {payload.get()} | Headers: {headers.get_headers()}")
        
        response = requests.post("https://datanodes.to/download", data=payload.get(), headers=headers.get_headers())
        
        url = str(response.json()['url'])
        
        logging.info(f"Found Direct Download Link: {url}")
        
        return {"url": url, "payload": None, "headers": None, "method": "get"}
    
    @staticmethod
    def gofile(url) -> str:
        logging.info("Downloader:gofile Generating download link using gofile this may take up to 2 Minutes")
        _id = url.split("/")[-1]
        with sync_playwright() as p:
            logging.info("Downloader:gofile Launching playwright Instance (Chromium)")
            # Launch the browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            link = ""
            accounttoken = ""

            def on_response(response):
                nonlocal link, page, browser, _id
                if response.url.startswith(f"https://api.gofile.io/contents/{_id}?"):
                    logging.info("Downloader:gofile Data Retrieved")
                    try:
                        
                        data = json.loads(response.text())
                        file = list(data["data"]['children'].keys())[0]
                        link = data["data"]['children'][file]["link"]
                        print(link)
                    except Exception as e:
                        logging.error(f"Downloader:gofile Failed to get response body: {e}")
                        
            page.on("response", on_response)

            logging.info(f"Downloader:gofile Visiting {url} for Direct Download Link extraction")
            page.goto(url)
            
            logging.info("Downloader:gofile Waiting until successfull link and cookie extraction if this take longer then 2 Minutes please close the Programm")
            
            while not link and not accounttoken:
                page.wait_for_timeout(1000)
                
                if not accounttoken:
                    cookies = context.cookies()
                    for cookie in cookies:
                        if cookie["name"] == "accountToken":
                            accounttoken = cookie["value"]
                            logging.info(f"Downloader:gofile Successfull found Cookie: {accounttoken}")
            
            logging.info(f"Downloader:gofile Successfull found link: {link}")
            
            page.close()
            browser.close()
            return {"url": link, "payload": None, "headers": {"Cookie": f"accountToken={accounttoken}"}, "method": "get"}

class Downloader:
    @staticmethod
    def steamrip(url, data):
        try:
            response = requests.get(url)
            
            response.raise_for_status()
            
            page_content = response.text
            
            for i in page_content.split("script"):
                if "DOWNLOAD" in i:
                    logging.debug(i)
                    pass
            
            logging.info("Downloader:steamrip Extracting downloadable links")
            
            found_links = {}
            
            for key, data in data["steamrip"]["provider"].items():

                regex_finder = re.findall(data["pattern"], page_content)
                
                if regex_finder and len(regex_finder) == 1:
                    found_links[key] = data["formaturl"].format(detected_link = regex_finder[0])
                else:
                    found_links[key] = None
            
            logging.info(f"Downloader:steamrip Detected download links: {found_links}")
            
            logging.info(f"Downloader:steamrip Generating Filename")
            try:
                name = url[:-1].split("/")[-1].split("free-download")[0][:-1].replace("-","_")
            except:
                logging.warning("Downloader:steamrip Error while generating name continuing with random name")
                name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            
            return found_links, name
                
        except requests.RequestException as e:
            logging.error(f"Downloader:steamrip Error fetching the URL: {e}")

downloader_data = {
    "steamrip":{
        "provider": {
            "gofile": {
                "pattern": r"gofile\.io/d/([a-zA-Z0-9]+)",
                "formaturl": "https://gofile.io/d/{detected_link}",
                "priority": 1,
                "downloader": DirectLinkDownloader.gofile,
                "enabled": True
            },
            "filecrypt": {
                "pattern": r'<a\s+href="\/\/(?:\w+\.)?filecrypt\.\w+\/Container\/([A-Za-z0-9]+)"',
                "formaturl": "https://www.filecrypt.cc/Container/{detected_link}",
                "priority": 2,
                "downloader": DirectLinkDownloader.filecrypt,
                "enabled": False
            },
            "buzzheavier": {
                "pattern": r'<a\s+href="\/\/buzzheavier\.com\/([^"]+)"',
                "formaturl": "https://buzzheavier.com/{detected_link}",
                "priority": 4,
                "downloader": DirectLinkDownloader.buzzheavier,
                "enabled": True
            },
            "fichier": {
                "pattern": r'1fichier\.com/\?([^"]+)',
                "formaturl": "https://1fichier.com/?{detected_link}",
                "priority": 3,
                "downloader": DirectLinkDownloader.ficher,
                "enabled": True
            },
            "datanode": {
                "pattern": r'<a\s+href="\/\/datanodes\.to\/([^"]+)"',
                "formaturl": "https://datanodes.to/{detected_link}",
                "priority": 5,
                "downloader": DirectLinkDownloader.datanode,
                "enabled": True
            },
            "megadb": {
                "pattern": r'<a\s+href="\/\/megadb\.net\/([^"]+)"',
                "formaturl": "https://megadb.net/{detected_link}",
                "priority": 6,
                "downloader": DirectLinkDownloader.megadb,
                "enabled": False
            },
        },
        "method": Downloader.steamrip,
        "compression": "rar",
    }
}

def _generate_master_key(url):
    for key, items in downloader_data.items():
        
        if key in url:
            
            __function = downloader_data[key]["method"]
            __master_key = key
            
            logging.info(f"Downloader {key} detected")
            
            break
    
    return __function, __master_key

def _get_best_downloader(urls: dict, master_key: str):
    __best_downloader, __best_downloader_key = None, None
    
    for key, download_link in urls.items():
        if not downloader_data[master_key]["provider"][key]["enabled"]:
            logging.warning(f"Downloader:main Provider: {key} is currently disabled")
            continue
        
        if download_link != None:
            if __best_downloader == None:
                
                __best_downloader = downloader_data[master_key]["provider"][key]
                __best_downloader_key = key
                
                continue
            
            if downloader_data[master_key]["provider"][key]["priority"] < __best_downloader["priority"]:
                __best_downloader = downloader_data[master_key]["provider"][key]
                __best_downloader_key = key
    
    return __best_downloader, __best_downloader_key

def _download(url, payload, headers, filename, method, master_key):
    
    with requests.Session() as session:
        
        logging.info(f'Downloader:main Requesting {url} with method: {method}')
        if method == "post":
            response = session.post(url, headers=headers, data=payload, stream=True)
        
        elif method == "get":
            response = session.get(url, headers=headers, data=payload, stream=True, allow_redirects=True)
        
        else:
            logging.error("Downloader:main Data is missing")
            
        response.raise_for_status()
        
        total_size = round(int(response.headers.get('content-length', 0)) / 1073741824, 2)
        logging.info(f"Downloader:main File size: {total_size}GB")
        block_size = 1024
        
        # Start the download process
        with open(f"{os.getcwd()}/{TEMP_DIR}/{filename}.{downloader_data[master_key]['compression']}", "wb") as file:
            with tqdm(unit='B', unit_scale=True, desc="Downloading", ncols=100) as pbar:
                for data in response.iter_content(block_size):
                    file.write(data)
                    pbar.update(len(data))

def _steamrip_get_main_path() -> str:
    logging.info("Getting steamrip Main folder, also installing all requierements.")
    try:
        steamrip_data = load_json(os.path.join(os.getcwd(), CONFIG_DIR, STEAMRIP_JSON_NAME))
            
    except FileNotFoundError:
        logging.warning("No steamrip data detected creating")
            
        steamrip_data = {"commenredist": []}
            
        save_json(os.path.join(os.getcwd(), CONFIG_DIR, STEAMRIP_JSON_NAME), steamrip_data)
        
    __commen = ""
            
    for file in os.listdir(os.path.join(os.getcwd(), TEMP_DIR)):
        if "_commonredist" == file.lower():
            logging.info("Downloader:main Installs found")
            __commen = file
                
        elif os.path.isdir(os.path.join(os.getcwd(), TEMP_DIR, file)):
            __main_folder = file
        
    for file in os.listdir(os.path.join(os.getcwd(), TEMP_DIR, __commen)):
        if not file in steamrip_data['commenredist']:
            logging.info(f"Missing Commenredist: {file}")
            os.system(os.path.join(os.getcwd(), TEMP_DIR, __commen, file))
            steamrip_data["commenredist"].append(file)
            save_json(os.path.join(os.getcwd(), CONFIG_DIR, STEAMRIP_JSON_NAME),steamrip_data)
        
        logging.info("Commenredist installation successfull")

    return os.path.join(os.getcwd(), TEMP_DIR, __main_folder), __main_folder

class Extractor:
    @staticmethod
    def rar(rar_path):
        try:
            with rarfile.RarFile(rar_path) as rf:
                logging.info(f"Downloader:main Detected File: {rar_path}")
                logging.info("Downloader:main Generating Temp folder: temp")

                Folder.check_existence(os.getcwd(), TEMP_DIR)
                
                #winrar_path = 'C:\Program Files\WinRAR'
                
                #subprocess.run([winrar_path, 'x', rar_path, f'"{os.path.join(os.getcwd(), TEMP_DIR)}"'])
                #patoolib.extract_archive(rar_path, outdir=f'"{os.path.join(os.getcwd(), TEMP_DIR)}"')
                #Archive(rar_path).extractall(directory=os.path.join(os.getcwd(), TEMP_DIR))
                rf.extractall(os.path.join(os.getcwd(), TEMP_DIR))
                
                logging.info(f"Downloader:main Successfull Extracted to: {os.path.join(os.getcwd(), TEMP_DIR)}")
        
        except rarfile.Error as e:
            logging.error(f"Downloader:main Error while Extraction: {e}")

def _game_naming():
        game_folder, folder_name = _steamrip_get_main_path()
        
        if folder_name in os.listdir(os.path.join(os.getcwd(), GAME_DIR)):
            logging.info(f"Applying Patch for {folder_name}")
        
        Folder.move(game_folder, os.path.join(os.getcwd(), GAME_DIR))
        Folder.delete(os.path.join(os.getcwd(), TEMP_DIR))
        
        logging.info("Searching for every Executable file...")
        exes = []
        full_path_game_execution = None
        
        for name in os.listdir(os.path.join(os.path.join(os.getcwd(), GAME_DIR, folder_name))):
            if name.endswith(".exe"):
                if folder_name.replace(" ", "").lower() in name.replace(" ", "").lower():
                        full_path_game_execution = os.path.join(GAME_DIR, folder_name, name)
                        logging.info(f"Main game file detected: {full_path_game_execution}")
                        break
        
        if full_path_game_execution==None:
            for path, subdirs, files in os.walk(os.path.join(os.getcwd(), GAME_DIR, folder_name)):
                for name in files:
                    if name.endswith(".exe"):
                        exes.append(name)
                        if folder_name.replace(" ", "").lower() in name.replace(" ", "").lower():
                            full_path_game_execution = os.path.join(GAME_DIR, folder_name, name)
                            logging.info(f"Main game file detected: {full_path_game_execution}")
                        
                        else:
                            temp_name = ""
                            for part in folder_name.split(" "):
                                temp_name += part[0]

                            temp_name += ".exe"
                            
                            if temp_name == name:
                                pass
                                full_path_game_execution = os.path.join(GAME_DIR, folder_name, temp_name)
        if full_path_game_execution == None or not full_path_game_execution.endswith(".exe"):
            for file in exes:
                print(file)
                if not file.endswith(".exe"):
                    continue
                if "unity" in file.lower():
                    continue
                full_path_game_execution = os.path.join(GAME_DIR, folder_name, file)
                break
    
        return full_path_game_execution, folder_name

def _add_game_info(full_path_game_execution, folder_name):
        logging.debug(full_path_game_execution)
        
        if not File.check_existence(os.path.join(os.getcwd(), CONFIG_DIR), GAMES_JSON_DATA):
            save_json(os.path.join(os.getcwd(), CONFIG_DIR, GAMES_JSON_DATA), {"Games":{folder_name: {"args": [], "playtime": 0, "exe": full_path_game_execution}}})
        
        game_data = load_json(os.path.join(os.getcwd(), CONFIG_DIR, GAMES_JSON_DATA))
        
        if folder_name in game_data["Games"].keys():
            
            game_data["Games"][folder_name] = {"args": game_data["Games"][folder_name]["args"], "playtime": game_data["Games"][folder_name]["playtime"], "exe": full_path_game_execution}
        
        else:
            game_data["Games"][folder_name] = {"args": [], "playtime": 0, "exe": full_path_game_execution}
        
        save_json(os.path.join(os.getcwd(), CONFIG_DIR, GAMES_JSON_DATA), game_data)

def start(url):
    logging.info(f"Downloader:main Starting Download for: {url}")
    __function, __master_key = _generate_master_key(url)
    
    logging.info("Downloader:main Preparing function call")
    
    __links, __file_name = __function(url, downloader_data)
    
    __file_name_with_extension = __file_name + "." + downloader_data[__master_key]["compression"]
    
    logging.info("Downloader:main Checking for the best possible downloader")
    
    __best_downloader, __best_downloader_key = _get_best_downloader(__links, __master_key)
    
    if __best_downloader == None:
        logging.error("Could not find a Downloader")
        return None
    
    logging.info(f"Downloader:main Best downloader: {__best_downloader_key}")
    
    __downloader_function = __best_downloader["downloader"]
    
    logging.info("Downloader:main Successfull build downloader function")
    
    __download_request = __downloader_function(__links[__best_downloader_key])
    
    logging.info(f"Downloader:main Starting the Download with: {__download_request}")
    
    Folder.check_existence(os.getcwd(), "Temp")
    Folder.check_existence(os.getcwd(), "Games")
    Folder.check_existence(os.getcwd(), "Config")
    
    try:
        _download(__download_request ["url"], __download_request ["payload"], __download_request ["headers"], __file_name, __download_request ["method"], __master_key)
    
    except KeyboardInterrupt:
        logging.warning(f"Download interrupted by User")
        Folder.delete(os.path.join(os.getcwd(), TEMP_DIR))
        return None
        
    
    logging.info("Downloader:main Download finished")
    
    if downloader_data[__master_key]["compression"] == "rar":
        Extractor.rar(os.path.join(os.getcwd(), TEMP_DIR, __file_name_with_extension))
    
    else:
        logging.error("Downloader:main Could not extract invailid format")
    
    if __master_key == "steamrip":
        full_path_game_execution, folder_name = _game_naming()
        _add_game_info(full_path_game_execution, folder_name)

class UnknownFileHost(Exception):
    def __init__(self, url):
        # Call the base class constructor with the message
        super().__init__(f"Unkown Host: {url}")