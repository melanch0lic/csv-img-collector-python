import requests
from bs4 import BeautifulSoup
import csv
import os.path
from soupsieve import select_one
import time
from selenium import webdriver
import argparse
import aiohttp
import asyncio
from random import choice
from aiostream import stream

results = []


def _get_browser():
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.chrome.favicons", False)
    fp.set_preference("browser.chrome.site_icons", False)
    geckodriver_path = os.path.join(
        os.path.expanduser("~"), "csv-img-collector-python\\geckodriver.exe"
    )
    if not os.path.exists(geckodriver_path):
        raise RuntimeError(
            "Improperly configured. Expecting geckodriver executable in {}".format(
                geckodriver_path
            )
        )
    browser = webdriver.Firefox(executable_path=geckodriver_path, firefox_profile=fp)
    browser.set_window_size(1224, 768)
    return browser


browser_1 = _get_browser()
browser_2 = _get_browser()
browser_3 = _get_browser()


def save_image(url, url_type, column_name, keyword):
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    photo = response.content
    if not os.path.exists("images"):
        if url_type == "wiki." or url_type == "britannica.":
            file_dir = os.path.join(url_type + url[-3] + url[-2] + url[-1])
        else:
            file_dir = os.path.join(url_type + "jpg")
    else:
        if url_type == "wiki." or url_type == "britannica.":
            file_dir = os.path.join(
                "images", column_name, keyword, url_type + url[-3] + url[-2] + url[-1]
            )
        else:
            file_dir = os.path.join("images", column_name, keyword, url_type + "jpg")

    if response.status_code == 200:
        with open(
            file_dir,
            "wb",
        ) as f:
            f.write(photo)


async def upload_wiki(keyword, column_name):
    print("Starting to upload from wiki. keyword: {}".format(keyword))
    # TODO: Implement getting page and parsing
    start_recur = time.time()
    base_url = "https://en.m.wikipedia.org"
    html_1 = requests.get(base_url + "/wiki/" + keyword).text
    soup = BeautifulSoup(html_1, "html.parser")
    t = soup.select_one("a.image")

    html_2 = requests.get(base_url + t.attrs["href"])
    soup = BeautifulSoup(html_2.text, features="lxml")
    a = soup.select_one("div.fullImageLink")
    link = a.select_one("a")
    end_recur = time.time()
    await asyncio.sleep(end_recur - start_recur)
    yield ("wiki", keyword)

    save_image("https:" + link.attrs["href"], "wiki.", keyword, column_name)

    timeout = choice([2, 3, 4, 5])
    print("wiki: sleeping for {}s".format(timeout))
    await asyncio.sleep(timeout)


async def upload_brit(keyword, column_name):
    start_recur = time.time()
    print("Starting to upload from brit. keyword: {}".format(keyword))
    # TODO: Implement getting page and parsing
    base_url = "https://www.britannica.com/search?query="
    browser_1.get(base_url + keyword)
    img = browser_1.find_element_by_css_selector(".SearchFeature .grid.p-20 img")
    image_url = img.get_attribute("src")
    end_recur = time.time()
    await asyncio.sleep(end_recur - start_recur)
    yield ("brit", keyword)
    save_image(image_url, "britannica.", column_name, keyword)

    timeout = choice([2, 3, 4, 5])
    print("brit: sleeping for {}s".format(timeout))
    await asyncio.sleep(timeout)


async def upload_pexels(keyword, column_name):
    start_recur = time.time()
    print("Starting to upload from pexels. keyword: {}".format(keyword))
    base_url = "https://www.pexels.com/ru-ru/search/"
    browser_2.get(base_url + keyword)
    img = browser_2.find_element_by_css_selector("img.photo-item__img:first-child")
    image_url = img.get_attribute("src")
    end_recur = time.time()
    await asyncio.sleep(end_recur - start_recur)

    yield (
        "pexels",
        keyword,
    )
    save_image(image_url, "pexels.", column_name, keyword)

    timeout = choice([2, 3, 4, 5])
    print("pexels: sleeping for {}s".format(timeout))
    await asyncio.sleep(timeout)


async def upload_ccsearch(keyword, column_name):
    start_recur = time.time()
    print("Starting to upload from ccsearch. keyword: {}".format(keyword))
    base_url = "https://search.creativecommons.org/search?q="
    browser_3.get(base_url + keyword)
    img = browser_3.find_element_by_css_selector("img.search-grid_image:first-child")
    image_url = img.get_attribute("src")
    end_recur = time.time()
    await asyncio.sleep(end_recur - start_recur)

    yield (
        "ccsearch",
        keyword,
    )
    save_image(image_url, "ccsearch.", column_name, keyword)
    timeout = choice([2, 3, 4, 5])
    print("pexels: sleeping for {}s".format(timeout))
    await asyncio.sleep(timeout)


async def readCSV(csv_file_name, column_name):
    with open(csv_file_name) as File:
        reader = csv.DictReader(File)
        for row in reader:
            results.append(row)

    if column_name != "_void_":
        if column_name in results[0].keys():
            if not os.path.exists("images/" + column_name):
                os.makedirs("images/" + column_name)
            os.chdir("images/" + column_name)

            for i in results:
                if not os.path.exists(i[column_name]):
                    os.makedirs(i[column_name])
                    os.chdir(i[column_name])
                    combine = stream.merge(
                        upload_brit(i[column_name], column_name),
                        upload_wiki(i[column_name], column_name),
                        upload_pexels(i[column_name], column_name),
                    )
                    async with combine.stream() as streamer:
                        async for source, filename in streamer:
                            print(
                                "Saving. source: {}, filename: {}".format(
                                    source, filename
                                )
                            )
                    await asyncio.sleep(1)
                    print("Finished...")
                    os.chdir("..")
                elif os.path.exists(i[column_name]):
                    if len(os.listdir(i[column_name])) < 3:
                        os.chdir(i[column_name])
                        combine = stream.merge(
                            upload_brit(i[column_name], column_name),
                            upload_wiki(i[column_name], column_name),
                            upload_pexels(i[column_name], column_name),
                        )
                        async with combine.stream() as streamer:
                            async for source, filename in streamer:
                                print(
                                    "Saving. source: {}, filename: {}".format(
                                        source, filename
                                    )
                                )
                        await asyncio.sleep(1)
                        print("Finished...")
                        os.chdir("..")

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
                combine = stream.merge(
                    upload_brit(cell_name, col_name),
                    upload_wiki(cell_name, col_name),
                    upload_pexels(cell_name, col_name),
                )
                async with combine.stream() as streamer:
                    async for source, filename in streamer:
                        print(
                            "Saving. source: {}, filename: {}".format(source, filename)
                        )
                await asyncio.sleep(1)
                print("Finished...")
                os.chdir("..")
            elif os.path.exists(cell_name):
                if len(os.listdir(cell_name)) < 5:
                    os.chdir(cell_name)
                    combine = stream.merge(
                        upload_brit(cell_name, col_name),
                        upload_wiki(cell_name, col_name),
                        upload_pexels(cell_name, col_name),
                    )
                async with combine.stream() as streamer:
                    async for source, filename in streamer:
                        print(
                            "Saving. source: {}, filename: {}".format(source, filename)
                        )
                await asyncio.sleep(1)
                print("Finished...")
                os.chdir("..")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("csv_name", help="the name of the csv file we want to read")

    parser.add_argument("--column", help="the name of the column in csv file to take")

    args = parser.parse_args()

    if args.column == "_void_":
        asyncio.run(readCSV(args.csv_name, "_void_"))
    else:
        asyncio.run(readCSV(args.csv_name, args.column))
    browser_1.quit()
    browser_2.quit()
    browser_3.quit()


if __name__ == "__main__":
    main()
