#! /usr/bin/env python3

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os
import datetime

LINK = "https://www.forestclub.com.pl/wyszukaj/?flat-type=Mieszkanie&area=&room=&floor=#flats-list"


def load_more_offer(driver):
    while True:
        try:
            button = driver.find_element_by_css_selector('button.btn.load_more_offer')
            button.click()
        except:
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
    with open(file, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Apartment', 'Size', 'Rooms', 'Floor', 'Status', 'Link'])
        for apart in apartments:
            writer.writerow([apart['Apartment'], apart['Size'], apart['Rooms'],
                             apart['Floor'], apart['Status'], apart['Link']])


def stats_to_csv(file, apartments):
    flats_total = len(apartments)
    flats_free = len([x for x in apartments if x["Status"] == 'free'])
    flats_sold = len([x for x in apartments if x["Status"] == 'sold'])

    print(f"Total: {flats_total}, Free: {flats_free}, Sold: {flats_sold}")

    stats_date = datetime.date.today()
    with open(file, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        if os.stat(file).st_size == 0:
            writer.writerow(['Date', 'Flats total', 'Flats free', 'Flats sold'])
        writer.writerow([stats_date, flats_total, flats_free, flats_sold])


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(LINK)

    load_more_offer(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    apartments = find_apartments(soup)

    apartments_to_csv("apartments.csv", apartments)
    stats_to_csv("stats.csv", apartments)


if __name__ == '__main__':
    main()
