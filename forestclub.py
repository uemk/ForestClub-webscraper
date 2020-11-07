#! /usr/bin/env python3

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

LINK = "https://www.forestclub.com.pl/wyszukaj/?flat-type=Mieszkanie&area=&room=&floor=#flats-list"


def load_more_offer(driver):
    while True:
        try:
            button = driver.find_element_by_css_selector('button.btn.load_more_offer')
            button.click()
        except Exception:
            break


def apartments_to_csv(file, apartments):
    with open(file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for apart in apartments:
            writer.writerow([apart['Apartment'], apart['Size'], apart['Rooms'],
                             apart['Floor'], apart['Status'], apart['Link']])


def find_apartments(soup):
    apartments = []

    for flat in soup.find_all("tr", {"class": "active"}):
        apart = {}
        attributes = flat.text.strip().split('\n')

        apart['Apartment'] = attributes[0]
        apart['Size'] = attributes[1]
        apart['Rooms'] = attributes[2]
        apart['Floor'] = attributes[3]
        apart['Status'] = attributes[4]
        try:
            apart['Link'] = flat.a['href']
        except TypeError:
            apart['Link'] = None
        apartments.append(apart)

    return apartments


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(LINK)

    load_more_offer(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    apartments = find_apartments(soup)

    apartments_to_csv("test.csv", apartments)


if __name__ == '__main__':
    main()
