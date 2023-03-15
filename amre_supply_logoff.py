from bs4 import BeautifulSoup as bs
import csv
import requests
import re


letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
               'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']


PATH = "C:\Program Files (x86)\chromedriver.exe"


RELIABLE_BRANDS_LINK = "https://www.reliableparts.ca/brands"
AMRE_BRANDS_LINK = "https://www.amresupply.com/manufacturers?m="

def brands_by_letter(url):
    # WORKS WELL
    new_urls = []
    for i in range(len(letter_list)):
        temp = url + letter_list[i]
        new_urls.append(temp)
    return new_urls


def urls_for_threads(url):
    # WORKS (KINDA) WAAAAY TOO SLOW amre+reliableparts
    new_urls1 = []
    new_urls2 = []
    new_urls3 = []

    for i in range(9):
        temp1 = url + letter_list[i]
        temp2 = url + letter_list[i+9]
        temp3 = url + letter_list[i+18]
        new_urls1.append(temp1)
        new_urls2.append(temp2)
        new_urls3.append(temp3)
    return new_urls1, new_urls2, new_urls3


def get_brand_listing(url, sum):
    # WORKS WELL
    url = url + "/100000000/"
    result = requests.get(url)
    lk = 48
    all_urls = []

    all_urls.append(url)

    return all_urls


def print_result(numbers, names, prices, links, rep):
    for itr in range(rep):
        print("item # ", itr+1)
        print("link:", links[itr])
        print("number:", numbers[itr])
        print("name:", names[itr])
        print("price:", prices[itr])
        print("************************************************")



def amre_run():
    url = 'https://www.amresupply.com/manufacturers?m='
    manufacturers = url_changer(url)
    with open('info.csv', 'w', encoding="utf-8") as csvfile:
        fieldnames = ["link", "number", "name", "price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        summary = 0
        for i in range(len(manufacturers)):
            result = requests.get(manufacturers[i])
            soup = BeautifulSoup(result.text, 'lxml')
            manufacturer_url_list = get_manufacturer_urls(soup)
            for j in range(len(manufacturer_url_list)):
                result = requests.get(manufacturer_url_list[j] + "/100000000")
                soup = BeautifulSoup(result.text, 'lxml')
                numbers, names, prices, links, rep = get_product_info(soup)
                for itr in range(rep):
                    summary += 1
                    writer.writerow({'link': links[itr], 'number': numbers[itr], 'name': names[itr], 'price': prices[itr]})

        print("Writing complete, summary is: ", summary)


