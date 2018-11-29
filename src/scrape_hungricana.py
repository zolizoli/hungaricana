import time
import urllib.request
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
###############################################################################
#####              selenium functions getting our data                    #####
###############################################################################
opts = Options()
prefs = {'download.default_directory': '/home/developer/PycharmProjects/hungaricana/data/raw'}
opts.add_experimental_option('prefs', prefs)


def init_browser(url):
    browser = Chrome(options=opts)
    browser.get(url)
    save_button = browser.find_element_by_xpath('//*[@id="pdfview"]/div[1]/div[2]/div[1]/button/span')
    return browser, save_button



###############################################################################
#####                            setup                                    #####
###############################################################################
base_url = 'https://library.hungaricana.hu/hu/collection/fszek_budapesti_telefonkonyvek/?fbclid=IwAR3tV45AISWSxI3mTRnZ1wQnSq9byWkyMEUlXoE5ZS3YHfIop-2pRCcekqE'
req = urllib.request.Request(
    base_url,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)


with urllib.request.urlopen(req) as response:
    try:
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        books = soup.findAll('a')
        books = [e['href'] for e in books if e.has_attr('href')]
        books = [e for e in books if e.startswith('/hu/view')]
        books = ['https://library.hungaricana.hu' + e for e in books]
    except Exception as e:
        print(e)
tocrawl = []


def generate_urls(book):
    ending = '?pg=%s&layout=s'
    for i in range(0, 800):
        pagination = ending % i
        u = book + pagination
        tocrawl.append(u)

for book in books:
    generate_urls(book)

with open('data/logs/crawled.txt', 'r') as f:
    crawled = []
    for l in f:
        crawled.append(l.strip())

tocrawl = [e for e in tocrawl if e not in crawled]
of = open('data/logs/crawled.txt', 'a')


def download_page(page):
    try:
        browser, button = init_browser(page)
        of.write(page + '\n')
        button.click()
        time.sleep(1)
        ok = browser.find_element_by_name('ok')
        ok.click()
        time.sleep(4)
        browser.quit()
    except Exception as e:
        print(e)
        pass


with ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(download_page, tocrawl)
