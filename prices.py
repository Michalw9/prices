import requests
from bs4 import BeautifulSoup
import json
from gzip import decompress


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"


def products_urls_list_euro():
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
    page = 1
    list = []
    last_page = mex_max_urls()
    while page <= last_page:
        url = f"https://www.mediaexpert.pl/telewizory-i-rtv/telewizory?limit=200&page={page}"
        response = requests.get(url, headers={"User-Agent": user_agent})
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        for h2 in soup.findAll("h2"):
            list.append("https://www.mediaexpert.pl" + h2.a['href'])
        page = page + 1
    return list


def products_urls_list_msh():
    page = 1
    list = []
    last_page = msh_max_urls()
    while page <= last_page:
        url = f"https://mediamarkt.pl/rtv-i-telewizory/telewizory/wszystkie-telewizory?limit=50&page={page}"
        response = requests.get(url, headers={"User-Agent": user_agent})
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        a = soup.findAll("a",{"class": "count spark-link"}, href = True)
        for item in a:
            list.append("https://www.mediamarkt.pl" + item['href'][0:int((len(item['href'])-8))])
        page = page + 1
    return list

def find_price(store_page):
    page = requests.get(store_page, headers={"User-Agent": user_agent})
    soup = BeautifulSoup(page.text, 'html.parser')
    for tag in  soup.find_all("script", {"type":"application/ld+json"}):
        parsed = json.loads(tag.text)
        if "offers" in parsed and "price" in parsed["offers"] and 'name' in parsed:
            return [parsed['name'], parsed["offers"]["price"],parsed['gtin13']]             #[0] - Name [1] - Price [2] - EAN
    return None

print(products_urls_list_msh())
