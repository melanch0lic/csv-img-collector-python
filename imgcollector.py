import requests
from bs4 import BeautifulSoup
import csv
import os.path
from soupsieve import select_one
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

results = []


def upload_wiki(key_word, column_name):
    base_url = "https://en.m.wikipedia.org"
    html_1 = requests.get(base_url + "/wiki/" + key_word).text
    soup = BeautifulSoup(html_1, "html.parser")
    t = soup.select_one("a.image")

    time.sleep(2)

    html_2 = requests.get(base_url + t.attrs["href"])
    soup = BeautifulSoup(html_2.text, features="lxml")
    a = soup.select_one("div.fullImageLink")
    link = a.select_one("a")
    print(link.attrs["href"])

    time.sleep(2)

    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36"
    }
    response = requests.get(
        "https:" + link.attrs["href"], headers=headers)
    photo = response.content
    
    if not os.path.exists("images"):
        file_dir = os.path.join('wiki.' + link.attrs["href"][-3] + link.attrs["href"][-2] + link.attrs["href"][-1])
    else: file_dir = os.path.join(column_name, key_word,'wiki.' + link.attrs["href"][-3] + link.attrs["href"][-2] + link.attrs["href"][-1])

    if response.status_code == 200:
        with open(
            file_dir, "wb",
        ) as f:
            f.write(photo)

    time.sleep(2)

def _get_browser():
    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.chrome.favicons', False)
    fp.set_preference('browser.chrome.site_icons', False)
    print(os.getcwd()) 
    geckodriver_path = os.path.join(
        os.path.expanduser('~'),'csv-img-collector-python\\geckodriver.exe')
    if not os.path.exists(geckodriver_path):
        raise RuntimeError(
            'Improperly configured. Expecting geckodriver executable in {}'.format(geckodriver_path))
    browser = webdriver.Firefox(
        executable_path=geckodriver_path,
        firefox_profile=fp)
    browser.set_window_size(1224, 768)
    return browser


def upload_britannica(key_word, column_name):
    base_url = "https://www.britannica.com/search?query="
    browser = _get_browser()
    browser.get(base_url + key_word)
    img = browser.find_element_by_css_selector('.SearchFeature .grid.p-20 img')

    image_url = img.get_attribute('src')
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36"
    }
    response = requests.get(
        image_url, headers=headers)
    photo = response.content
    
    if not os.path.exists("images"):
        file_dir = os.path.join('britannica.' + image_url[-3] + image_url[-2] + image_url[-1])
    else: file_dir = os.path.join(column_name, key_word,'britannica.' + image_url[-3] + image_url[-2] + image_url[-1])

    if response.status_code == 200:
        with open(
            file_dir, "wb",
        ) as f:
            f.write(photo)

    time.sleep(2)


def upload_pexels(key_word, column_name):
    base_url = "https://www.pexels.com/ru-ru/search/"
    browser = _get_browser()
    browser.get(base_url + key_word)
    img = browser.find_element_by_css_selector('img.photo-item__img:first-child')

    image_url = img.get_attribute('src')
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36"
    }
    response = requests.get(
        image_url, headers=headers)
    photo = response.content
    
    if not os.path.exists("images"):
        file_dir = 'pexels.jpg'
    else: file_dir = os.path.join(column_name, key_word,'pexels.jpg')

    if response.status_code == 200:
        with open(
            file_dir, "wb",
        ) as f:
            f.write(photo)

    time.sleep(2)


def upload_ccsearch(key_word, column_name):
    base_url = "https://search.creativecommons.org/search?q="
    browser = _get_browser()
    browser.get(base_url + key_word)
    img = browser.find_element_by_css_selector('img.search-grid_image:first-child')

    image_url = img.get_attribute('src')
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36"
    }
    response = requests.get(
        image_url, headers=headers)
    photo = response.content
    
    if not os.path.exists("images"):
        file_dir = 'ccsearch.jpg'
    else: file_dir = os.path.join(column_name, key_word,'ccsearch.jpg')

    if response.status_code == 200:
        with open(
            file_dir, "wb",
        ) as f:
            f.write(photo)
    os.chdir("..")

    time.sleep(2)


def readCSV(csvfile_name, column_name):
    with open(csvfile_name) as File:
        reader = csv.DictReader(File)
        for row in reader:
            results.append(row)

    if column_name in results[0].keys():
        if not os.path.exists("images/" + column_name):
            os.makedirs("images/" + column_name)
        os.chdir("images/" + column_name)

        for i in results:
            if not os.path.exists(i[column_name]):
                os.makedirs(i[column_name])
                os.chdir(i[column_name])   
                upload_wiki(i[column_name], column_name)
                upload_britannica(i[column_name], column_name)
                upload_pexels(i[column_name], column_name) 
                upload_ccsearch(i[column_name], column_name)
            elif os.path.exists(i[column_name]):
                print(os.getcwd())  
                if len(os.listdir(i[column_name]))<5:
                    os.chdir(i[column_name]) 
                    upload_wiki(i[column_name], column_name)  
                    upload_britannica(i[column_name], column_name)
                    upload_pexels(i[column_name], column_name)
                    upload_ccsearch(i[column_name], column_name)  

    else:
        col_name = list(results[0].keys())[0]

        if not os.path.exists("images/" + col_name):
            os.makedirs("images/" + col_name)
        os.chdir("images/" + col_name)

        for i in results:
            cell_name = i[list(results[0].keys())[0]]
            if not os.path.exists(cell_name):
                os.makedirs(cell_name)
                os.chdir(cell_name)   
                upload_wiki(cell_name, col_name)
                upload_britannica(cell_name, col_name)
                upload_pexels(cell_name, col_name)
                upload_ccsearch(cell_name, col_name) 

            elif os.path.exists(cell_name):
                print(os.getcwd())  
                if len(os.listdir(cell_name))<5:
                    os.chdir(cell_name) 
                    upload_wiki(cell_name, col_name) 
                    upload_britannica(cell_name, col_name)
                    upload_pexels(cell_name, col_name)
                    upload_ccsearch(cell_name, col_name)    


def main():
    readCSV("animals.csv", "animal")


if __name__ == "__main__":
    main()
