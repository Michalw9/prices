import requests
from bs4 import BeautifulSoup
import json
from gzip import decompress


strona1 = "https://www.euro.com.pl/telewizory-led-lcd-plazmowe/sony-xr85z9jaep-8k-goole-tv-sony.bhtml"
strona2 = "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory/telewizor-lg-led-55nano883"
strona3 = "https://mediamarkt.pl/rtv-i-telewizory/telewizor-lg-oled55a13la"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

def products_urls_list_euro():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    sitemap_gz = requests.get("https://www.euro.com.pl/sitemap-produkty-rtv.xml.gz", headers={"User-Agent": user_agent})
    soup = BeautifulSoup(decompress(sitemap_gz.content), 'lxml')
    urls = soup.findAll("url")
    url_list=[]
    for item in urls:
        url_list.append(item.find("loc").text)
    return url_list


def msh_max_urls():
    url = "https://mediamarkt.pl/rtv-i-telewizory/telewizory/wszystkie-telewizory?limit=50&page=1"
    response = requests.get(url, headers={"User-Agent": user_agent})
    soup = BeautifulSoup(response.content, "lxml")
    x = soup.find("span", {"class": "from"})
    return int(x.text.split()[1])

def mex_max_urls():
    url = "https://www.mediaexpert.pl/telewizory-i-rtv/telewizory?limit=200&page=1"
    response = requests.get(url, headers={"User-Agent": user_agent})
    soup = BeautifulSoup(response.content, "lxml")
    x = soup.find("span", {"class": "from"})
    return int(x.text.split()[1])

def products_urls_list_mex():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    page = 1
    list = []
    last_page = mex_max_urls()
    while page <= last_page:
        url = f"https://www.mediaexpert.pl/telewizory-i-rtv/telewizory?limit=200&page={page}"
        response = requests.get(url, headers={"User-Agent": user_agent})
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        for h2 in soup.find_all("h2"):
            list.append("https://www.mediaexpert.pl" + h2.a['href'])
        page = page + 1
    return list


def products_urls_list_msh():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    page = 1
    last_page = msh_max_urls()
    list = []
    while page <= last_page:
        url = f"https://mediamarkt.pl/rtv-i-telewizory/telewizory/wszystkie-telewizory?limit=50&page={page}"
        response = requests.get(url, headers={"User-Agent": user_agent})
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        for h2 in soup.find_all("h2"):
            list.append("https://www.mediaexpert.pl" + h2.a['href'])
        page = page + 1
    return list

def find_price(store_page):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    page = requests.get(store_page, headers={"User-Agent": user_agent})
    soup = BeautifulSoup(page.text, 'html.parser')
    for tag in  soup.find_all("script", {"type":"application/ld+json"}):
        parsed = json.loads(tag.text)
        if "offers" in parsed and "price" in parsed["offers"] and 'name' in parsed:
            return [parsed['name'], parsed["offers"]["price"],parsed['gtin13']]             #[0] - Name [1] - Price [2] - EAN
    return None

for page in products_urls_list_mex()[:20]:
    print(find_price(page))



