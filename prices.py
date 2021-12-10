import requests
from bs4 import BeautifulSoup
import json

strona1 = "https://www.euro.com.pl/telewizory-led-lcd-plazmowe/sony-xr85z9jaep-8k-goole-tv-sony.bhtml"
strona2 = "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory/telewizor-lg-led-55nano883"
strona3 = "https://mediamarkt.pl/rtv-i-telewizory/telewizor-lg-oled55a13la"

def find_price(store_page):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    page = requests.get(store_page, headers={"User-Agent": user_agent})
    soup = BeautifulSoup(page.text, 'html.parser')
    for tag in  soup.find_all("script", {"type":"application/ld+json"}):
        parsed = json.loads(tag.text)
        if "offers" in parsed and "price" in parsed["offers"] and 'name' in parsed:
            return [parsed['name'], parsed["offers"]["price"],parsed['gtin13']]             #[0] - Name [1] - Price [3] - EAN
    return None
print(find_price(strona1))
