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


def find_apartments(soup):
    apartments = []

    for flat in soup.find_all("tr", {"class": "active"}):
        apart = {}
        attributes = flat.text.strip().split('\n')

        apart['Apartment'] = attributes[0]
        apart['Size'] = float(attributes[1].split()[0])
        apart['Rooms'] = int(attributes[2].split()[0])
        if attributes[3].strip() == 'parter':
            apart['Floor'] = 0
        else:
            apart['Floor'] = int(attributes[3].split()[1])

        if attributes[4] == 'wolne':
            apart['Status'] = 'free'
        else:
            apart['Status'] = 'sold'

        try:
            apart['Link'] = flat.a['href']
        except TypeError:
            apart['Link'] = None
        apartments.append(apart)

    return apartments


def apartments_to_csv(file, apartments):
    with open(file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Apartment', 'Size', 'Rooms', 'Floor', 'Status', 'Link'])
        for apart in apartments:
            writer.writerow([apart['Apartment'], apart['Size'], apart['Rooms'],
                             apart['Floor'], apart['Status'], apart['Link']])


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
