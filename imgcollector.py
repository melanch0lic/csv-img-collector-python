import requests
from bs4 import BeautifulSoup
import csv
import os.path
from soupsieve import select_one

results = []


def upload_wiki(keyword, column_name):  # ВИКИПЕДИЯ
    base_url = "https://en.m.wikipedia.org"
    html_1 = requests.get(base_url + "/wiki/" + keyword).text
    soup = BeautifulSoup(html_1, "html.parser")
    t = soup.select_one("a.image")

    html_2 = requests.get(base_url + t.attrs["href"])
    soup = BeautifulSoup(html_2.text, features="lxml")
    a = soup.select_one("div.fullImageLink")
    link = a.select_one("a")
    print(link.attrs["href"])

    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.2.195 Yowser/2.5 Safari/537.36"
    }
    photo = requests.get(
        "https:" + link.attrs["href"], headers=headers).content
    with open(
        "images/" + column_name + "/" + keyword + "." +
        link.attrs["href"][-3] +
        link.attrs["href"][-2] + link.attrs["href"][-1], "wb",
    ) as f:
        f.write(photo)


def readCSV(csvfile_name, column_name):
    with open(csvfile_name) as File:
        reader = csv.DictReader(File)
        for row in reader:
            results.append(row)
    if column_name in results[0].keys():
        if not os.path.exists("images/" + column_name):
            os.chdir("images")
            os.mkdir(column_name)
            current_file_name = column_name
        for i in results:
            upload_wiki(i[column_name], column_name)


def main():
    readCSV("animals.csv", "animal")


if __name__ == "__main__":
    main()
