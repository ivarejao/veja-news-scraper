# Code made in Pycharm by Igor Varejao

import os
import locale
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing import Pool
from pathlib import Path
from argparse import ArgumentParser
import requests
# from lxml import etree

DATA_PATH = Path("/home/ivarejao/Neologism/data")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--sector', help='Setor a ser listado', required=False, default='all')
    parser.add_argument('--time-range', help='Intervalo de tempo a ser procurado', default=[2008, 2023], nargs='+', type=int)
    parser.add_argument('--by-month', help='Se habilitado as notícias serão salvos por mês', const='store_true', nargs='?')

    args = parser.parse_args()
    if args.time_range is not None and len(args.time_range) > 2:
        raise ValueError("Para especificar o ano é necessário apenas informar 1 ou 2 anos")
    return args


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

def create_session():

    login_url = 'https://veja.abril.com.br/login'

    session = requests.Session()

    # Prepare the login data
    login_data = {
        "email": 'anaself@gmail.com',
        "password": 'Neoscopio23',
    }

    # Perform the login
    session.post(login_url, data=login_data)

    return session

def read_year(y : int, sector : str) -> None:
    print(f"Looking at year:{y}")
    file = []
    log = []
    root_dir = DATA_PATH / sector 

    # Ensure that all directories exists
    os.makedirs(root_dir / "links", exist_ok=True)
    os.makedirs(root_dir / "news", exist_ok=True)
    os.makedirs(root_dir / "log", exist_ok=True)

    session = create_session()

    with open(root_dir / f"links/{y}.txt", "r") as r:
        lines = r.readlines()
    with tqdm(total=len(lines)) as pb:
        for idx, link in enumerate(lines):
            try:
                response = session.get(link.replace('\n', ''))
                if response.status_code == 200:
                    soup_page = BeautifulSoup(response.text, 'html.parser')
                    try:
                        readNews(idx, soup_page, file, log)
                        pb.update()
                    except Exception as e:
                        print(e)
                else:
                    print(f"Something went wrong with the request of {link}")
            except Exception as e:
                print(e)

    with open(root_dir / f"log/log_{y}.txt", "w") as log_file, \
                open(root_dir / f"news/{y}.txt", "w") as news:
        log_file.write("".join(log))
        news.write("".join(file))
    print("\033[92m Done! \033[0m")


def main():
    args = parse_args()

    sector = args.sector

    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil

    # Set time-range
    if len(args.time_range) > 1:
        start = args.time_range[0]
        end = args.time_range[1]
        years = list(range(start, end+1))
        years_str = f"[{start}, {end}]" # Just for log
    else:
        years = args.time_range
        years_str = years[0]

    print("Começando a coleta das notícias")
    print(f"Setor: {sector} ")
    print(f"Intervalo de tempo: {years_str}")
    print("---")

    for y in years:
        read_year(y, sector)

if __name__ == "__main__":
    main()
