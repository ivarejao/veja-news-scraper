# Code made in Pycharm by Igor Varejao

import locale
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool
# from lxml import etree
import re

sector="tecnologia"

def readNews(soup, file, log):
    post_header = soup.find_all("div", {"class": "post-header"})[0]
    content = soup.find_all("section", {"class": "content"})[0]
    # / html / body / div[1] / article / div[1]
    # html.veja body.post-template-default.single.single-post.postid-513435.single-format-standard.esporte div.container article  # post-513435.article.post div.post-header
    title = str(post_header.find("h1").string)
    file.append(f"{title}"+'\n')


    # date_elem = post_header.find_element(by=By.CLASS_NAME, value="author")
    # date = date_elem.find_element(by=By.TAG_NAME, value="span").text
    # log.append(f"({date})Reading[{i}]: {title}\n")

    try:
        description = str(post_header.find("h2").string)
        file.append(description + "\n")
    except Exception as e:
        log.append(e.__str__())

    content_list = content.find_all("p")

    # content_section = driver.find_element(by=By.CLASS_NAME, value="content")
    # list_p = content_section.find_elements(by=By.TAG_NAME, value="p")
    list_p = content_list[:-3]
    for p in list_p:
        file.append(p.text)
    file.append("\n\n")

def save_news(content, y):
    with open(f"../data/{sector}/news/news-{y}.txt", "a") as news:
        news.write("".join(content))
def save_logs(log, y):
    with open(f"../data/{sector}/log/log-{y}.txt", "a") as log_file:
        log_file.write("".join(log))

def get_year(content):
    describe = content.find("span", {"class" : "author"})
    # year = describe.contents[3].contents[0].split()[2][:-1]
    year = re.findall("20[0-2][0-9]", describe.contents[3].contents[0])
    return year[0]

def read_all(links):
    # Se precisar fazer parcialmentea coleta
    links = links[:]
    last_year = 0
    file = []
    log = []
    with tqdm(total=len(links)) as pb:
        for link in links:
            try:
                with urlopen(link) as url:
                    page = url.read().decode("utf8")
                soup_page = BeautifulSoup(page, 'html.parser')
                restricted_soup = soup_page.find_all("div", {"class": "container"})[1]
                y = get_year(restricted_soup)
                # if (len(file) > 40):
                #     print(f"Saving {last_year}")
                #     save_news(file, last_year)
                #     save_logs(log, last_year)
                #     file = []
                #     log = []
                #     exit(1)
                if last_year != y:
                    if last_year != 0:
                        print(f"Saving {last_year}")
                        save_news(file, last_year)
                        save_logs(log, last_year)
                        file = []
                        log = []
                    print(f"Looking at year:{y}")
                try:
                    readNews(restricted_soup, file, log)
                except Exception as e:
                    print("[1]"+e.__str__())
                last_year = y
            except Exception as e:
                print("[2]"+e.__str__())
            pb.update()

    print("\033[92m Done! \033[0m")


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil
with open(f"../data/{sector}/links.txt", "r") as r:
    lines = r.readlines()
read_all(lines)
