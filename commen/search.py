from . import re
from . import requests

STEAMRIP = "https://steamrip.com/{start}{middel}/"
STEAMRIP_NAME = "steamrip"
STEAMRIP_INDICATOR = '<h1 class="page-title">Search Results for: <span>{search}/</span>'
#                     <h1 class="page-title">Search Results for: <span>Company of heroes 2/</span></h1>
SEARCH_STRING = "?s="

FILTER = ["categoryopen-world", "top-games", "updated-games","games-list","steps-for-games","contact-us","terms-and-conditions","privacy-policy", "#"]

class Searcher:
    def __init__(self, method = STEAMRIP_NAME):
        self.method = method
        
        if self.method == STEAMRIP_NAME:
            self.url = STEAMRIP
    
    def search(self, string):
        search_url = "https://steamrip.com/?s=" + string.replace(" ", "+")
        req = requests.get(search_url).text
        if self.method == STEAMRIP_NAME:
            
            
            pattern = r'<a href="([^"]+)" class'
            
            results = []
            
            data_searched = re.findall(pattern, req)
            if not data_searched:
                print("Error in DATA:", req)

            for part in data_searched:
                if not "free-download" in part:
                    pass
                
                if part in FILTER:
                    continue
                
                extracted = {"name": part.replace("/", "").split("-free-down")[0], "link": f"https://steamrip.com/{part}"}
                if extracted not in results:
                    results.append(extracted)
            
        return results
    
   #"href="turnip-boy-robs-a-bank-free-download-t1/"