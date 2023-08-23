# Code made in Pycharm by Igor Varejao
import time
import threading
import tqdm
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
import locale
from time import sleep
import logging
import itertools
import sys
import os
from pathlib import Path

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write('\rDone!     ')

def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def readNews(i, file):
    title_elem = driver.find_element(by=By.CLASS_NAME, value="title")
    print(f"Reading[{i}]: {title_elem.text}")
    description = driver.find_element(by=By.CLASS_NAME, value="description")
    content_section = driver.find_element(by=By.CLASS_NAME, value="content")
    list_p = content_section.find_elements(by=By.TAG_NAME, value="p")
    list_p = list_p[:-3]

    file.write(title_elem.text + "\n")
    file.write(description.text + "\n")
    for p in list_p:
        file.write(p.text)
    file.write("\n\n")
    print()


def displayAllNews(driver):
    count = 0
    while True:
        for i in range(5):
            try:
                element_news_list = driver.find_element(by=By.ID, value='infinite-list')
                break
            except:
                pass
        news_list = element_news_list.find_elements(by=By.XPATH, value="//*[starts-with(@id, 'post')]")
        news = news_list[-1]
        scroll_shim(driver, news)
        ActionChains(driver).move_to_element(news).perform()

        try:
            more = driver.find_element(by=By.ID, value="infinite-handle")
            btn = more.find_element(by=By.TAG_NAME, value="button")
            if btn.is_displayed():
                btn.click()
            else:
                print("Something went wrong")
                break
            count = 0
        except Exception as e:
            print(e)
            count += 1
            if count == 10:
                break
                # resp = input("Continue? [y/n]")
                # if (resp.lower() == "n"):
                #     break
        sleep(1)

sector="cultura"
# Create dir where will be stored the links files
TARGET_PATH = Path("../data/{sector}")
os.makedirs(TARGET_PATH, exist_ok=True)

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil
# Start session
options = webdriver.FirefoxOptions()
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
# Do not show web brownser
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
driver = webdriver.Firefox(options=options)
#driver = webdriver.Firefox()
print("Online")

driver.get(f"https://veja.abril.com.br/{sector}/")
log = logging.getLogger(__name__)
log.info(f"Looking at {sector}")

done = False
t_read = threading.Thread(target=displayAllNews, args=[driver])
t_loading = threading.Thread(target=animate)

t_read.start()
t_loading.start()
t_loading.join()
done = True
t_loading.join()

# Trying to zoom out
# from selenium.webdriver import Keys
# ActionChains(driver.find_element(By.TAG_NAME("html"))).key_down(Keys.CONTROL).key_down(Keys.SUBTRACT).perform()

element_news_list = driver.find_element(by=By.ID, value='infinite-list')
news_list = element_news_list.find_elements(by=By.XPATH, value="//*[starts-with(@id, 'post')]")
with open(TARGET_PATH / "links_2023_1.txt", "w") as f, \
        tqdm.tqdm(total=len(news_list)) as pb:
    for n in news_list:
        link = n.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        f.write(link + "\n")
        pb.update(1)
