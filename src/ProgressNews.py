# Code made in Pycharm by Igor Varejao

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
import locale
from time import sleep
from tqdm import tqdm



def readNews(i):
    post_header = driver.find_element(by=By.CLASS_NAME, value="post-header")
    title = post_header.find_element(by=By.CLASS_NAME, value="title").text
    file.append(f"{title}"+'\n')

    date_elem = post_header.find_element(by=By.CLASS_NAME, value="author")
    date = date_elem.find_element(by=By.TAG_NAME, value="span").text
    log.append(f"({date})Reading[{i}]: {title}\n")

    try:
        description = driver.find_element(by=By.CLASS_NAME, value="description")
        file.append(description.text + "\n")
    except Exception as e:
        log.append(e.__str__())

    content_section = driver.find_element(by=By.CLASS_NAME, value="content")
    list_p = content_section.find_elements(by=By.TAG_NAME, value="p")
    list_p = list_p[:-3]
    for p in list_p:
        file.append(p.text)
    file.append("\n\n")

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil
driver = webdriver.Firefox()
years = list(range(2015, 2018))

for y in years:
    print(f"Looking at year:{y}")
    file = []
    log = []
    try:
        with open(f"../data/links-{y}.txt", "r") as r:
            lines = r.readlines()
            with tqdm(total=len(lines)) as pb:
                for idx, link in enumerate(lines):
                    driver.get(url=link)
                    # driver.execute_script(f"location.href='{link}';")
                    readNews(idx)
                    pb.update()
    except Exception as e:
        print(e)

    with open(f"../log/log-{y}.txt", "w") as log_file, \
                open(f"../data/show-news-{y}.txt", "w") as news:
        log_file.write("".join(log))
        news.write("".join(file))
