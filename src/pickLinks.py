# Code made in Pycharm by Igor Varejao

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
import locale
from time import sleep

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
    from time import sleep
    i = 0
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
        except Exception as e:
            print(e)
            print("Done")
            break
        sleep(1)

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Set locale to brasil
# Start session
# options = webdriver.FirefoxOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('headless')
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()
# driver = webdriver.Chrome()

years = [2014]
years = list(range(2022, 2023))

for y in years:
    driver.get(f"https://veja.abril.com.br/{y}/")
    print(f"Looking at year:{y}")
    displayAllNews(driver)

    element_news_list = driver.find_element(by=By.ID, value='infinite-list')
    news_list = element_news_list.find_elements(by=By.XPATH, value="//*[starts-with(@id, 'post')]")
    with open(f"../data/show-links-{y}.txt", "w") as f:
        for n in news_list:
            link = n.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            f.write(link + "\n")