from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
               'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9']


PATH = "C:\Program Files (x86)\chromedriver.exe"
login = "login"
password = "password"


def url_changer(url):
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


def get_manufacturer_all(session, url):
    result = session.get(url+"/100000000", cookies=session.cookies)
    soup = BeautifulSoup(result.text, 'lxml')
    numbers, names, prices, links, rep = get_product_info(soup)

    return links, numbers, names, prices, rep


def get_manufacturer_urls(soup):
    # RETURNS ALL LINKS TO MANUFACTURERS' PAGES (WORKS, DON'T TOUCH) amre
    all_urls = []
    i = 0
    for tag in soup.find_all(["div"], class_="col-md-2 col-sm-3 col-xs-6 brandImage"):
        for a in tag.find_all('a', href=True):
            i += 1
            all_urls.append(a['href'])
    print(i)

    return all_urls


def get_product_info(soup):
    # READY AND WORKING(DON'T TOUCH)
    numbers = []
    names = []
    prices = []
    links = []
    rep = 0

    for form in soup.find_all(["form"]):
        for tag3 in form.find_all(["span"], class_="parts-modal-number"):
            rep += 1
            numbers.append(tag3.text)
        for div in form.find_all(["div"], class_="noPadding"):
            for a in div.find_all('a', href=True):
                names.append(a['title'])
                links.append(a['href'])
        for tag2 in form.find_all(["div"], class_="product-price"):
            price = tag2.text
            price = price.translate({ord(i): None for i in 'ADTOCR '})
            prices.append(price)
            #print(price)

    print(rep)
    return numbers, names, prices, links, rep


def print_result(numbers, names, prices, links, rep):
    for itr in range(rep):
        print("item # ", itr+1)
        print("link:", links[itr])
        print("number:", numbers[itr])
        print("name:", names[itr])
        print("price:", prices[itr])
        print("************************************************")


def amre_run():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    #options.headless = True
    # driver = webdriver.Chrome(options=options, executable_path=PATH)
    serv = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")

    # LOG IN TO THE SITE
    driver1 = webdriver.Chrome(service=serv, options=options)
    driver2 = webdriver.Chrome(service=serv, options=options)
    driver3 = webdriver.Chrome(service=serv, options=options)

    driver1.get("https://www.amresupply.com/login")
    driver2.get("https://www.amresupply.com/login")
    driver3.get("https://www.amresupply.com/login")

    log_in1 = driver1.find_element("name", "accountNumber")
    log_in2 = driver2.find_element("name", "accountNumber")
    log_in3 = driver3.find_element("name", "accountNumber")

    log_in1.send_keys(login)
    log_in2.send_keys(login)
    log_in3.send_keys(login)

    pass_in1 = driver1.find_element("name", "password")
    pass_in2 = driver2.find_element("name", "password")
    pass_in3 = driver3.find_element("name", "password")

    pass_in1.send_keys(password)
    pass_in2.send_keys(password)
    pass_in3.send_keys(password)

    pass_in1.send_keys(Keys.RETURN)
    pass_in2.send_keys(Keys.RETURN)
    pass_in3.send_keys(Keys.RETURN)
    # LOGIN END
    #driver.close()

    url = 'https://www.amresupply.com/manufacturers?m='
    manufacturers = url_changer(url)
    man1 = manufacturers[0]
    man2 = manufacturers[1]
    man3 = manufacturers[2]

    with open('info.csv', 'w', encoding="utf-8") as csvfile:
        fieldnames = ["link", "number", "name", "price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(9):
            driver1.get(man1[i])
            driver2.get(man2[i])
            driver3.get(man3[i])
            soup1 = BeautifulSoup(driver1.page_source, 'lxml')
            soup2 = BeautifulSoup(driver2.page_source, 'lxml')
            soup3 = BeautifulSoup(driver3.page_source, 'lxml')

            manufacturer_url_list1 = get_manufacturer_urls(soup1)
            manufacturer_url_list2 = get_manufacturer_urls(soup2)
            manufacturer_url_list3 = get_manufacturer_urls(soup3)
            for j in range(len(manufacturer_url_list1)):
                driver1.get(manufacturer_url_list1[j] + "/100000000")
                soup = BeautifulSoup(driver1.page_source, 'lxml')
                numbers, names, prices, links, rep = get_product_info(soup)
                for itr in range(rep):
                    writer.writerow({'link': links[itr], 'number': numbers[itr], 'name': names[itr], 'price': prices[itr]})
            for j in range(len(manufacturer_url_list2)):
                driver1.get(manufacturer_url_list2[j] + "/100000000")
                soup = BeautifulSoup(driver2.page_source, 'lxml')
                numbers, names, prices, links, rep = get_product_info(soup)
                for itr in range(rep):
                    writer.writerow({'link': links[itr], 'number': numbers[itr], 'name': names[itr], 'price': prices[itr]})
            for j in range(len(manufacturer_url_list3)):
                driver3.get(manufacturer_url_list3[j] + "/100000000")
                soup = BeautifulSoup(driver1.page_source, 'lxml')
                numbers, names, prices, links, rep = get_product_info(soup)
                for itr in range(rep):
                    writer.writerow({'link': links[itr], 'number': numbers[itr], 'name': names[itr], 'price': prices[itr]})
                    #time.sleep(rep/1000)
                #print_result(numbers, names, prices, links, rep)

    print("Writing complete")

    driver.quit()
