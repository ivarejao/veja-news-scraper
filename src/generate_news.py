import os
import locale
import threading
from time import sleep
from pathlib import Path
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from dotenv import load_dotenv


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--sector", help="Setor a ser listado", required=False, default="all")
    parser.add_argument(
        "--time-range", help="Intervalo de tempo a ser procurado", default=[2008, 2023], nargs="+", type=int
    )
    parser.add_argument(
        "--data-path",
        help="Localização do diretório com os links e onde será armezado as notícias",
        default=f"{os.environ['PWD']}/data",
    )

    args = parser.parse_args()
    if args.time_range is not None and len(args.time_range) > 2:
        raise ValueError("Para especificar o ano é necessário apenas informar 1 ou 2 anos")
    return args


def readNews(i, soup, file, log):
    post_header = soup.find_all("div", {"class": "post-header"})[0]
    content = soup.find_all("section", {"class": "content"})[0]

    title = str(post_header.find("h1").string)
    file.append(f"{title}" + "\n")

    try:
        description = str(post_header.find("h2").string)
        file.append(description + "\n")
    except Exception as e:
        log.append(e.__str__())

    content_list = content.find_all("p")
    list_p = content_list[:-3]
    for p in list_p:
        file.append(p.text)
    file.append("\n\n")


def create_session():
    login_url = "https://veja.abril.com.br/login"
    load_dotenv()  # load the `VEJA_EMAIL` and `VEJA_PASSWORD` enviroment variables

    session = requests.Session()

    # Prepare the login data
    login_data = {
        "email": os.environ["VEJA_EMAIL"],
        "password": os.environ["VEJA_PASSWORD"],
    }

    # Perform the login
    session.post(login_url, data=login_data)

    return session


def read_year(y: int, sector: str, data_path: str) -> None:
    file = []
    log = []
    root_dir = data_path / sector

    # Ensure that all directories exists
    os.makedirs(root_dir / "links", exist_ok=True)
    os.makedirs(root_dir / "news", exist_ok=True)
    os.makedirs(root_dir / "log", exist_ok=True)

    session = create_session()

    with open(root_dir / f"links/{y}.txt", "r") as r:
        lines = r.readlines()
    with tqdm(total=len(lines), desc=f"Year {y}: ", unit="news") as pb:
        for idx, link in enumerate(lines):
            try:
                response = session.get(link.replace("\n", ""), allow_redirects=False)
                if response.status_code == 200:
                    soup_page = BeautifulSoup(response.text, "html.parser")
                    try:
                        readNews(idx, soup_page, file, log)
                        pb.update()
                    except Exception as e:
                        print(e)
                else:
                    log.append(f"Something went wrong with the request of {link}")
            except Exception as e:
                print(e)

    with open(root_dir / f"log/log-{y}.txt", "w") as log_file, open(root_dir / f"news/news-{y}.txt", "w") as news:
        log_file.write("".join(log))
        news.write("".join(file))
    # print("\033[92m Done! \033[0m")


def main():
    args = parse_args()

    sector = args.sector
    data_path = Path(args.data_path)

    locale.setlocale(locale.LC_ALL, "pt_BR.utf8")  # Set locale to brasil

    # Set time-range
    if len(args.time_range) > 1:
        start = args.time_range[0]
        end = args.time_range[1]
        years = list(range(start, end + 1))
        years_str = f"[{start}, {end}]"  # Just for log
    else:
        years = args.time_range
        years_str = years[0]

    print("Começando a coleta das notícias")
    print(f"Setor: {sector} ")
    print(f"Intervalo de tempo: {years_str}")
    print("---")

    threads = []
    # TODO: Apply the concurrent strategy with multiple threads
    for y in years:
        t = threading.Thread(target=read_year, args=(y, sector, data_path))
        t.start()
        threads.append(t)
        sleep(1)
        # read_year(y, sector, data_path)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
