# Code made in Pycharm by Igor Varejao
import os
from colored import fg, bg, attr
import locale
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool
# from lxml import etree
import re


def readNews(i, soup, file_record, log, month) -> str:
    all_months = {"jan", "fev", "mar", "abr", "Maio", "jun", "jul",
            "ago", "set", "out", "nov", "dez"}

    post_header = soup.find_all("div", {"class": "post-header"})[0]
    try:
        author_div = soup.find("span", {"class": "author"})
        #print(author_div)
        num_spans = len(author_div.find_all("span"))
        date_str = author_div.find_all("span")[-1].string
        # Caso tenha 'Atualizado' e 'Publicado'
        date_str = date_str.split("-")[-1]
        #print(f"{fg(1)} {date_str} {attr('reset')}")
        # Procurar um modo de melhorar essa busca
        for m in all_months:
            if re.search(m, date_str):
                month = m
        #print(date_str)
        #result = date_str.split(" - ")
        #if len(result) == 1:
        #    month = date_str.split(" ")[1]
        #else: 
        #    month = result[1].split(" ")[3]
    except Exception as e:
        pass
    content = soup.find_all("section", {"class": "content"})[0]
    # / html / body / div[1] / article / div[1]
    # html.veja body.post-template-default.single.single-post.postid-513435.single-format-standard.esporte div.container article  # post-513435.article.post div.post-header
    title = str(post_header.find("h1").string)
    
    news_record = list()
    news_record.append(f"{title}"+'\n')

    # date_elem = post_header.find_element(by=By.CLASS_NAME, value="author")
    # date = date_elem.find_element(by=By.TAG_NAME, value="span").text
    # log.append(f"({date})Reading[{i}]: {title}\n")

    try:
        description = str(post_header.find("h2").string)
        news_record.append(description + "\n")
    except Exception as e:
        log.append(e.__str__())

    content_list = content.find_all("p")

    # content_section = driver.find_element(by=By.CLASS_NAME, value="content")
    # list_p = content_section.find_elements(by=By.TAG_NAME, value="p")
    list_p = content_list[:-3]
    for p in list_p:
        news_record.append(p.text)
    news_record.append("\n\n")

    # Caso mês já tenha sido visto, adiciona a notícia
    # caso contrário, cria um novo campo
    if month in file_record:
        file_record[month].extend(news_record)
    else:
        file_record[month] = news_record
    
    return month

def read_year(y):
    print(f"Looking at year:{y}")
    file_record = dict()
    log = []
    with open(f"../data/all/links/{y}.txt", "r") as r:
        lines = r.readlines()
    lines = lines[18212:20933] #
    lines.reverse()
    with tqdm(total=len(lines)) as pb:
        month = "jan"
        for idx, link in enumerate(lines):
            try:
                with urlopen(link) as url:
                    page = url.read().decode("utf8")
                soup_page = BeautifulSoup(page, 'html.parser')
                restricted_soup = soup_page.find_all("div", {"class": "container"})[1]
                old_month = month
                try:
                    month = readNews(idx, restricted_soup, file_record, log, month)
                    pb.update()

                    if old_month != month:
                        print(f"{fg('blue')}Mudando do mês {old_month} para o mês {month} {attr('reset')}")
                except Exception as e:
                    pb.total = pb.total - 1
            except Exception as e:
                pb.total = pb.total - 1
            #if idx >= 25:
            #    break

    #with open(f"../log/log-{y}.txt", "w") as log_file:
    #   log_file.write("".join(log))
    news_root_dir = f"../data/all/news/{y}-change"
    if not os.path.exists(news_root_dir):
        os.mkdir(news_root_dir)

    for month in list(file_record.keys()):
        with open(f"{news_root_dir}/{month}.txt", "w") as news:
            news.write("".join(file_record[month]))
    
    print(f"{bg(2)}{attr(1)}        {attr('reset')}")
    print(f"{bg(2)}{attr(1)}  Done  {attr('reset')}")
    print(f"{bg(2)}{attr(1)}        {attr('reset')}")


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil
years = list([2012, 2014, 2016, 2018, 2020, 2022])
years = [2022]
# years = [2014, 2016]
# years = [2017, 2019]
# years = [2020, 2021]
# years = [2022]

for y in years:
    read_year(y)
