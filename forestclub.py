#! /usr/bin/env python3

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import os
import datetime
import my_gmail
from dotenv import load_dotenv

# requires .env file with the following format (sender & recipient to be replaced by proper usernames):
# FROM_EMAIL="sender@gmail.com"
# TO_EMAIL="recipient@gmail.com"
load_dotenv()
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")

LINK = "https://www.forestclub.com.pl/wyszukaj/?flat-type=Mieszkanie&area=&room=&floor=#flats-list"
APART_PATH = "apartments.csv"
STATS_PATH = "stats.csv"


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
    stats = {'flats_total': len(apartments),
             'flats_free': len([x for x in apartments if x["Status"] == 'free']),
             'flats_sold': len([x for x in apartments if x["Status"] == 'sold'])}

    print(f"Total: {stats['flats_total']}, Free: {stats['flats_free']}, Sold: {stats['flats_sold']}")

    stats_date = datetime.date.today()
    with open(file, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        if os.stat(file).st_size == 0:
            writer.writerow(['Date', 'Flats total', 'Flats free', 'Flats sold'])
        writer.writerow([stats_date, stats['flats_total'], stats['flats_free'], stats['flats_sold']])


def check_stats_change(file):
    data = []
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row:
                data.append(row)

    # compare the stats and send relevant notifications ny e-mail
    if len(data) >= 3:  # if there are previous status to compare with
        data[-1].pop(0)  # remove date info
        data[-2].pop(0)  # remove date info
        last = data[-1]
        before_last = data[-2]
        if last == before_last:
            print("No changes since last time")
        else:
            if last[0] > before_last[0]:
                email_subject = 'New apartments available'
            elif last[0] == before_last[0]:
                if last[2] > before_last[2]:
                    email_subject = 'Some apartment(s) sold'
                else:
                    email_subject = 'Some apartments returned to market'
            else:
                email_subject = 'Total number of apartments decreased'

            email_text = f"Please check the web page {LINK} or local {APART_PATH} file"

            my_gmail.create_and_send_email(FROM_EMAIL, TO_EMAIL, "[ForestClub] "+email_subject, email_text)
            print("Notification e-mail sent!")
    else:
        print("No previous stats to compare with")


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(LINK)

    load_more_offer(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    apartments = find_apartments(soup)

    apartments_to_csv(APART_PATH, apartments)
    stats_to_csv(STATS_PATH, apartments)
    check_stats_change(STATS_PATH)


if __name__ == '__main__':
    main()
