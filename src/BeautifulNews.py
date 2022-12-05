# Code made in Pycharm by Igor Varejao

import locale
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool
# from lxml import etree



def readNews(i, soup, file, log):
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

def read_year(y):
    print(f"Looking at year:{y}")
    file = []
    log = []
    with open(f"../data/links-{y}.txt", "r") as r:
        lines = r.readlines()
    with tqdm(total=len(lines)) as pb:
        for idx, link in enumerate(lines):
            try:
                with urlopen(link) as url:
                    page = url.read().decode("utf8")
                soup_page = BeautifulSoup(page, 'html.parser')
                restricted_soup = soup_page.find_all("div", {"class": "container"})[1]
                try:
                    readNews(idx, restricted_soup, file, log)
                    pb.update()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

    with open(f"../log/log-{y}.txt", "w") as log_file, \
                open(f"../data_beatiful/news-{y}.txt", "w") as news:
        log_file.write("".join(log))
        news.write("".join(file))
    print("\033[92m Done! \033[0m")


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil
years = list([2012, 2014, 2016, 2018, 2020, 2022])
years = [2012]
# years = [2014, 2016]
# years = [2017, 2019]
# years = [2020, 2021]
# years = [2022]

for y in years:
    read_year(y)
