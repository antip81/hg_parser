from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

import math
import requests
import time


def main():
    url = "https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?cena_d_from=400&cena_d_to=600&cena_d_unit=4&oglasivac_nekretnine_id_l=387237&nacin_placanja_id_l=387273"
    temp = get_list_of_apartments(url)
    print(get_apartment_data(temp[10]))
    # push_list_to_google_sheet()


# takes an url string with some searching conditions on hg
# returns a list of links for every apartment in given url
def get_list_of_apartments(search_url: str) -> list:
    # init chrome
    # open url in browser
    # passes page source for BS
    browser = webdriver.Chrome()
    browser.get(search_url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # need to wait till whole page has been loaded
    time.sleep(3)

    # finds all urls for apartments on page 1
    links = soup.find_all("h3", class_="product-title")

    # makes a list of links
    result = []
    for link in links:
        result.append(f"https://www.halooglasi.com{link.find('a').attrs['href']}")

    # takes a number of search results
    # calculates number of pages with results
    results_count = soup.find("div", class_="ad-faceting-result-count").find("em").contents
    number_of_pages = math.ceil(int(results_count[0]) / 20)

    # makes a loop from page=2 til the last page
    for page in range(2, number_of_pages + 1):
        # makes url for a page
        # finds all urls for apartments on a page
        page_url = f"{search_url}&page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all("h3", class_="product-title")

        # adds links to a list
        for link in links:
            result.append(f"https://www.halooglasi.com{link.find('a').attrs['href']}")

    # returns a list with all apartments urls from all pages
    return result


# takes apartment_url and returns a dict with price/square/phone/publicshed parameters for this apartment
def get_apartment_data(apartment_url: str) -> dict:
    # init
    # clicks a button to reveal phone number
    browser = webdriver.Chrome()
    browser.get(apartment_url)
    browser.find_element(By.TAG_NAME, "em").click()

    # need to wait till whole page has been loaded
    time.sleep(3)

    # passes source to bs
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # gets parameters - price/phone/pubished/square
    price = int(soup.find("span", class_="offer-price-value").contents[0])
    phone = soup.find("div", class_="col-sm-10 bold-15 contact-advertiser-details right-phone-1").find("a").attrs[
                "href"][4:]
    published = datetime.strptime(str(soup.find("strong", id="plh82").contents), "['%d.%m.%Y. u %H:%M']")
    square = str(soup.find("span", id="plh11").contents)[2:4]

    # returns a dict with params
    return {"price": price, "phone": phone, "published": str(published), "square": square}


def push_list_to_google_sheet():
    ...

if __name__ == '__main__':
    main()