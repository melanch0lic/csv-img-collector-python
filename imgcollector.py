import glob
from time import sleep
import csv
import os.path
from soupsieve import select_one
import time
import argparse
import aiohttp
import asyncio
import glob
from time import sleep
import csv
import os.path
from soupsieve import select_one
import time
import argparse
import aiohttp
import asyncio
from random import choice
from aiostream import stream
from urllib import parse
from selenium import webdriver
import requests


def get_image(image_url):
    response = requests.get(image_url)
    # FIXME: handle error status code.
    filename = os.path.basename(parse.urlparse(image_url).path)
    _, ext = os.path.splitext(filename)
    if not ext and response.headers.get("Content-Type"):
        # Try to get from headers.
        ext_by_mimetype = response.headers["Content-Type"].split("/")[-1]
        if ext_by_mimetype in ["jpg", "jpeg", "png"]:
            # FIXME: Improve the list of supported extensions.
            filename = "{}.{}".format(filename, ext_by_mimetype)
    content = response.content
    return filename, content


async def upload_wiki(keywords):
    if not hasattr(upload_wiki, "browser"):
        upload_wiki.browser = _get_browser()

    loop = asyncio.get_running_loop()

    def fetch_keyword(keyword):
        try:
            base_url = "https://en.m.wikipedia.org"
            upload_wiki.browser.get(base_url + "/wiki/" + keyword)
            link = upload_wiki.browser.find_element_by_css_selector(
                "a.image"
            ).get_attribute("href")
            upload_wiki.browser.get(link)
            image_url = upload_wiki.browser.find_element_by_css_selector(
                "div.fullImageLink img"
            ).get_attribute("src")
            sleep(1)
            return get_image(image_url)
        except Exception as exc:
            # FIXME: To log.
            print("wiki exception: {}".format(exc))
            return None, None

    for keyword in keywords:
        print("Starting to upload wiki/{}".format(keyword))
        # blocking example:
        # filename, content = fetch_keyword(keyword)
        filename, content = await loop.run_in_executor(
            None,
            fetch_keyword,
            keyword)
        yield ("wiki", keyword, filename, content)
        timeout = choice([2, 3, 4, 5])
        print("wiki: sleeping for {}s".format(timeout))
        await asyncio.sleep(timeout)


async def upload_britannica(keywords):
    if not hasattr(upload_britannica, "browser"):
        upload_britannica.browser = _get_browser()

    def fetch_keyword(keyword):
        try:
            base_url = "https://www.britannica.com/search?query="
            upload_britannica.browser.get(base_url + keyword)
            img = upload_britannica.browser.find_element_by_css_selector(
                ".SearchFeature .grid.p-20 img"
            )
            image_url = img.get_attribute("src")
            # Get image content.
            sleep(1)
            response = requests.get(image_url)
            # FIXME: handle error status code.
            content = response.content
            filename = os.path.basename(parse.urlparse(image_url).path)
            return filename, content
        except Exception as exc:
            # FIXME: To log.
            print("britannica exception: {}".format(exc))
            return None, None

    loop = asyncio.get_running_loop()
    for keyword in keywords:
        print("Starting to upload britannica/{}".format(keyword))
        # Blocking example for debugging:
        # filename, content = fetch_image_url(keyword)
        filename, content = await loop.run_in_executor(
            None,
            fetch_keyword,
            keyword)
        yield ("britannica", keyword, filename, content)
        timeout = choice([2, 3, 4, 5])
        await asyncio.sleep(timeout)


async def upload_pexels(keywords):
    if not hasattr(upload_pexels, "browser"):
        upload_pexels.browser = _get_browser()

    def fetch_keyword(keyword):
        # Get image content.
        try:
            base_url = "https://www.pexels.com/ru-ru/search/"
            upload_pexels.browser.get(base_url + keyword)
            img = upload_pexels.browser.find_element_by_css_selector(
                "img.photo-item__img:first-child"
            )
            image_url = img.get_attribute("src")
            sleep(1)
            return get_image(image_url)
        except Exception as exc:
            # FIXME: To log.
            print("pexels exception: {}".format(exc))
            return None, None

    loop = asyncio.get_running_loop()
    for keyword in keywords:
        print("Starting to upload pexels/{}".format(keyword))
        # blocking example:
        # filename, content = fetch_keyword(keyword)
        filename, content = await loop.run_in_executor(
            None,
            fetch_keyword,
            keyword)
        yield ("pexels", keyword, filename, content)
        timeout = choice([2, 3, 4, 5])
        await asyncio.sleep(timeout)


async def upload_ccsearch(keywords):
    if not hasattr(upload_ccsearch, "browser"):
        upload_ccsearch.browser = _get_browser()

    def fetch_keyword(keyword):
        # Get image content.
        try:
            base_url = "https://search.creativecommons.org/search?q="
            upload_ccsearch.browser.get(base_url + keyword)
            img = upload_ccsearch.browser.find_element_by_css_selector(
                "img.search-grid_image:first-child"
            )
            image_url = img.get_attribute("src")
            sleep(1)
            return get_image(image_url)
        except Exception as exc:
            # FIXME: to log
            print("ccsearch exception - {}".format(exc))
            return None, None

    loop = asyncio.get_running_loop()
    for keyword in keywords:
        print("Starting to upload ccsearch/{}".format(keyword))
        # blocking example for debugging:
        # filename, content = fetch_keyword(keyword)
        filename, content = await loop.run_in_executor(
            None,
            fetch_keyword,
            keyword)
        yield ("ccsearch", keyword, filename, content)
        timeout = choice([2, 3, 4, 5])
        await asyncio.sleep(timeout)


async def read_csv(csv_file_name, column_name=None):
    if not os.path.exists("images"):
        os.makedirs("images")
    rows = []
    sources = {
        "britannica": set(),
        "wiki": set(),
        "pexels": set(),
        "ccsearch": set()}
    with open(csv_file_name) as File:
        reader = csv.DictReader(File)
        all_columns = reader.fieldnames
        if column_name and column_name not in all_columns:
            raise ValueError(
                "Unknown column name. Excected one from {} got {} instead.".format(
                    all_columns, column_name
                )
            )
        column_name = column_name or all_columns[0]
        for row in reader:
            rows.append(row)
            keyword = row[column_name]
            if not os.path.exists(os.path.join("images", keyword)):
                os.makedirs(os.path.join("images", keyword))
            for source in sources:
                image_pattern = "{}.*".format(os.path.join(
                    "images",
                    keyword,
                    source
                    )
                    )
                if not glob.glob(image_pattern):
                    # No image from that source exist. Should upload.
                    sources[source].add(row[column_name])
    streams = [
        upload_britannica(sources["britannica"]),
        upload_wiki(sources["wiki"]),
        upload_pexels(sources["pexels"]),
        upload_ccsearch(sources["ccsearch"]),
    ]
    combine = stream.merge(*streams)
    async with combine.stream() as streamer:
        async for source, keyword, filename, content in streamer:
            if filename and content:
                new_filename = "{}{}".format(
                    source,
                    os.path.splitext(filename)[1])
                local_path = os.path.join("images", keyword, new_filename)
                with open(local_path, "wb") as f:
                    f.write(content)
                print("Successfully saved. {}/{}".format(source, keyword))
            else:
                print("Failed. {}/{}".format(source, keyword))
    for method in [
        upload_britannica,
        upload_wiki,
        upload_pexels,
        upload_ccsearch
    ]:
        try:
            if hasattr(method, "browser"):
                method.browser.quit()
        except Exception:
            # FIXME: Log error.
            pass
    print("Finished...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "csv_name",
        help="the name of the csv file we want to read")
    parser.add_argument(
        "--column",
        help="the name of the column in csv file to take")
    args = parser.parse_args()
    asyncio.run(read_csv(args.csv_name, column_name=args.column))


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
    browser = webdriver.Firefox(
        executable_path=geckodriver_path,
        firefox_profile=fp)
    browser.set_window_size(1224, 768)
    return browser


if __name__ == "__main__":
    main()