from . import re, logging
from . import requests
from . import commen

STEAMRIP = "https://steamrip.com/{start}{middel}/"
STEAMRIP_NAME = "steamrip"
STEAMRIP_INDICATOR = '<h1 class="page-title">Search Results for: <span>{search}/</span>'
#                     <h1 class="page-title">Search Results for: <span>Company of heroes 2/</span></h1>
SEARCH_STRING = "?s="

FILMPALAST_PATTERN = 'filmpalast\.to\/stream\/[A-Za-z0-9-]+'

FILMPALAST_URL = "https://filmpalast.to/search/title/"

FILTER = ["categoryopen-world", "top-games", "updated-games","games-list","steps-for-games","contact-us","terms-and-conditions","privacy-policy", "#"]

class Searcher:
    def __init__(self, method = STEAMRIP_NAME):
        logging.info(f"Init Searcher with method: {method}")
        self.method = method
        
        if self.method == STEAMRIP_NAME:
            self.url = STEAMRIP
    
    def search(self, string, games = False, film = False, series = False):
        results = []
        
        logging.info(f"Searching for: {string} with games: {games}, film: {film}, series: {series}")
        
        if games:
            logging.info(f"Starting search with: {string}")
            search_url = "https://steamrip.com/?s=" + string.replace(" ", "+")
            req = requests.get(search_url).text
            if True:
                
                
                pattern = r'<a href="([^"]+)" class'
                
                data_searched = re.findall(pattern, req)
                if not data_searched:
                    print("Error in DATA:", req)

                for part in data_searched:
                    if not "free-download" in part:
                        pass
                    
                    if part in FILTER:
                        continue
                    
                    extracted = {"name": "GAME: " + part.replace("/", "").split("-free-down")[0], "link": f"https://steamrip.com/{part}", "type": "game"}
                    if extracted not in results:
                        results.append(extracted)
        
        if film:
            search_url = FILMPALAST_URL + string.replace(" ", "%20")
            
            req = requests.get(search_url).text
            
            regex_match = re.findall(FILMPALAST_PATTERN, req)
            for match in regex_match:
                extracted = {"name": f"MOVIE: {match.split('/')[2]}", "link": f"https://{match}", "type": "film"}
                if extracted not in results:
                    results.append(extracted)
            
            
        return results
    
   #"href="turnip-boy-robs-a-bank-free-download-t1/"