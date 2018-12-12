from urllib.parse import urlencode
from webbrowser import open as browser
from fire import Fire

def search(string, engine="http://google.com/search"):
    browser(f"{engine}?{urlencode({'q': string})}")

if __name__ == "__main__":
    Fire(search)