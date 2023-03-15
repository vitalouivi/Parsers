from bs4 import BeautifulSoup
import csv
import requests
import string
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"
login = "login"
password = "password"


def paging(soup):
    for tag in soup.find_all(["div"], class_="col-md-6 col-xs-12"):
        for p in tag.find_all(["p"], class_="displayingProducts"):
            if (p.text == None):
                pages = 1
                print("0")
                return pages
            else:
                res = p.text
                res = res.replace("1 - 48", "")
                res = res.translate({ord(i): None for i in ' DisplayngProductf'})
                pages = int(res) // 48
                print(pages)
                return pages


def get_manufacturer_all(session, url):
    url = url +"/48/"
    result = session.get(url)
    soup = BeautifulSoup(result.text, 'lxml')
    ctr = paging(soup)
    lk = 48
    if isinstance(ctr, int):
        for itr in range(ctr):
            lk = itr * 48
            if lk == 0:
                new_url = url + ""
            new_url = url + str(lk)
            result = session.get(new_url)
            soup = BeautifulSoup(result.text, 'lxml')
            numbers, names, prices, links, rep = get_product_info(soup)
            itr += 1

            new_url = url + str(lk)
    else:
        result = session.get(url)
        soup = BeautifulSoup(result.text, 'lxml')
        numbers, names, prices, links, rep = get_product_info(soup)

    return links, numbers, names, prices, rep


def get_manufacturer_urls(soup):
    # RETURNS ALL LINKS TO MANUFACTURERS' PAGES (WORKS, DON'T TOUCH) reliable
    all_urls = []
    i = 0

    for tag in soup.find_all(["div"], class_="col-md-2 col-sm-4 col-xs-6 brandImage"):
        for a in tag.find_all('a', href=True):
            i += 1
            all_urls.append(a['href'])

    for tag in soup.find_all(["div"], class_="col-md-3 col-sm-6 col-xs-12 text-center"):
        for a in tag.find_all('a', href=True):
            i += 1
            all_urls.append(a['href'])
    #print(i)

    return all_urls


def get_product_info(soup):
    # READY AND WORKING(DON'T TOUCH)
    numbers = []
    names = []
    prices = []
    links = []
    rep = 0

    for form in soup.find_all(["form"]):
        for prc in form.find_all(["div"], class_="product-price"):
            rep += 1
            price = prc.text
            price = price.translate({ord(i): None for i in ' ADTOCRadtocr '})
            price = re.sub(r"\s+|^\s+|\s+$|\n+|^\n+|\n+$|\r+|^\r+|\r+$|\t+|^\t+|\t+$", "", price)  # | for OR condition +\t+^\t+|\t+$+\n+\r+^\r
            prices.append(price)
        for lk in form.find_all(["a"], class_="productName"):
            links.append(lk['href'])
            names.append(lk['title'])
        for num in form.find_all(["div"], class_="item-details"):
            numbers.append(num.text)
     #print(rep)
    return numbers, names, prices, links, rep


def print_result(numbers, names, prices, links, rep):
    for itr in range(rep):
        print("item # ", itr+1)
        print("link:", links[itr])
        print("number:", numbers[itr])
        print("name:", names[itr])
        print("price:", prices[itr])
        print("************************************************")


def reliable_run():

    with requests.Session() as s:x
        url = 'https://www.reliableparts.ca/brands'
        with open('info.csv', 'w', encoding="utf-8") as csvfile:
            fieldnames = ["link", "number", "name", "price"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            summary = 0
            result = s.get(url)
            soup = BeautifulSoup(result.text, 'lxml')
            manufacturer_url_list = get_manufacturer_urls(soup)
            for j in range(len(manufacturer_url_list)):
                print(manufacturer_url_list[j])
                result = s.get(manufacturer_url_list[j])
                soup = BeautifulSoup(result.text, 'lxml')
                numbers, names, prices, links, rep = get_manufacturer_all(s, manufacturer_url_list[j])
                for itr in range(rep):
                    summary += 1
                    writer.writerow({'link': links[itr], 'number': numbers[itr], 'name': names[itr], 'price': prices[itr]})
                    #print_result(numbers, names, prices, links, rep)

