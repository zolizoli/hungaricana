import time
import random
import urllib.request

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
###############################################################################
#####              selenium functions getting our data                    #####
###############################################################################
with open("src/proxies.txt", "r") as infile:
    proxies = infile.read().split("\n")

proxies = [e for e in proxies if e]
print(proxies)


def init_browser(url, iprotate=False):
    opts = Options()
    prefs = {
        'download.default_directory': '/home/zoltanvarju/PycharmProjects/hungaricana/data/raw'}
    opts.add_experimental_option('prefs', prefs)
    # opts.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    if iprotate:
        proxy = random.choice(proxies)
        opts.add_argument(f"--proxy-server=http://{proxy}")
    browser = Chrome(options=opts)
    browser.get(url)
    try:
        save_button = browser.find_element_by_xpath('//*[@id="pdfview"]/div[1]/div[2]/div[1]/button/span')
    except Exception as e:
        print("init browser", e)
        save_button = ""
    return browser, save_button



###############################################################################
#####                            setup                                    #####
###############################################################################
base_url = 'https://library.hungaricana.hu/hu/collection/fszek_budapesti_telefonkonyvek/?fbclid=IwAR3tV45AISWSxI3mTRnZ1wQnSq9byWkyMEUlXoE5ZS3YHfIop-2pRCcekqE'

try:
    browser, _ = init_browser(base_url, iprotate=False)
    time.sleep(3)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    books = soup.findAll('a')
    books = [e['href'] for e in books if e.has_attr('href')]
    books = [e.strip() for e in books if "view/" in e]
    books = [e.replace("../..", "/hu") for e in books]
    books = ['https://library.hungaricana.hu' + e for e in books]
    print(books)
    browser.quit()
except Exception as e:
    books = []
    print("getting links", e)
tocrawl = []


def generate_urls(book):
    ending = '?pg=%s&layout=s'
    for i in range(0, 800):
        pagination = ending % i
        u = book + pagination
        tocrawl.append(u)


if books:
    for book in books:
        generate_urls(book)
else:
    print("there is no book")

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
        time.sleep(15)
        button.click()
        time.sleep(15)
        # browser.switch_to_frame(browser.find_elements_by_tag_name("iframe")[0])
        try:
            browser.find_element_by_id("recaptcha-anchor").click()
        except Exception as e:
            pass
        try:
            browser.find_element_by_id("rc-anchor").click()
        except Exception as e:
            pass
        time.sleep(5)
        ok = browser.find_element_by_name('ok')
        ok.click()
        time.sleep(5)
        browser.quit()
    except Exception as e:
        print(e)
        pass

download_page("https://library.hungaricana.hu/hu/view/FszekCimNevTarak_20_00_1920/?pg=404&layout=s")

#
# with ThreadPoolExecutor(max_workers=20) as executor:
#     executor.map(download_page, tocrawl)
