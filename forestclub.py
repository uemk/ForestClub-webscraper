#! /usr/bin/env python3

"""
Scrapes and parses specific website with apartments
and triggers sending a notification e-mail if some statistics
concerning apartments available on the website have been changed since last time
"""

import os
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import my_gmail  # own module to handle Gmail API

# search link for apartments
_LINK = 'https://www.forestclub.com.pl/wyszukaj/?flat-type=Mieszkanie&area=&room=&floor=#flats-list'


def load_more_offer(driver: webdriver.Chrome) -> None:
    """
    Expands the web page to show all available offers
    by clicking proper button with selenium web-driver.
    """
    while True:
        button = driver.find_element_by_css_selector('button.btn.load_more_offer')
        if button.is_displayed():
            button.click()
        else:
            break


def find_apartments(soup: BeautifulSoup) -> list:
    """
    Finds all apartments in parsed webpage (BeautifulSoup object)
    and saves them in the list of dictionaries.
    """
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
            apart['Link'] = ''
        apartments.append(apart)

    return apartments


def apartments_to_csv(file: str, apartments: list) -> None:
    """
    Saves loaded apartments in a csv file.
    """
    with open(file, 'w+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Apartment', 'Size', 'Rooms', 'Floor', 'Status', 'Link'])
        for apart in apartments:
            writer.writerow([apart['Apartment'], apart['Size'], apart['Rooms'],
                             apart['Floor'], apart['Status'], apart['Link']])


def stats_to_csv(file: str, apartments: list) -> None:
    """
    Saves statistics concerning number of apartments (total, free, sold) in a csv file.
    """
    stats = {'flats_total': len(apartments),
             'flats_free': len([x for x in apartments if x["Status"] == 'free']),
             'flats_sold': len([x for x in apartments if x["Status"] == 'sold'])}

    print(f"Total: {stats['flats_total']}, "
          f"Free: {stats['flats_free']}, "
          f"Sold: {stats['flats_sold']}")

    stats_date = datetime.date.today()
    with open(file, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        if os.stat(file).st_size == 0:
            writer.writerow(['Date', 'Flats total', 'Flats free', 'Flats sold'])
        writer.writerow([stats_date, stats['flats_total'],
                         stats['flats_free'], stats['flats_sold']])


def check_stats_change(file: str) -> bool:
    """
    Compares the new statistics concerning number of apartments with the previous ones
    and triggers sending properly formatted e-mail if statistics have been changed since last time.
    """
    data = []
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row:
                data.append(row)

    # compare the stats and send relevant notifications by e-mail
    if len(data) >= 3:  # if there are previous status to compare with
        data[-1].pop(0)  # remove date info
        data[-2].pop(0)  # remove date info
        last = data[-1]
        before_last = data[-2]

        if last == before_last:
            print('No changes since last time')
            return False

        if last[0] > before_last[0]:
            email_subject = 'New apartments available'
        elif last[0] == before_last[0]:
            if last[2] > before_last[2]:
                email_subject = 'Some apartment(s) sold'
            else:
                email_subject = 'Some apartments returned to market'
        else:
            email_subject = 'Total number of apartments decreased'

        email_text = f'Please check the web page {_LINK} and local statistics file'

        # requires .env file
        load_dotenv()
        from_email = os.getenv('FROM_EMAIL')
        to_email = os.getenv('TO_EMAIL')

        my_gmail.create_and_send_email(from_email, to_email,
                                       '[ForestClub] '+email_subject, email_text)

        print('Notification e-mail sent!')
        return True

    print('No previous stats to compare with')
    return False


def main() -> None:
    """
    Triggers the functions to load all apartment offers from a given website, parse the website,
    save found apartments and statistics in corresponding csv files,
    send notification email if statistics were different than the last time.
    """

    apart_path = 'apartments.csv'  # path to save information about apartments
    stats_path = 'stats.csv'  # path to save statistics

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(_LINK)

    load_more_offer(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    apartments = find_apartments(soup)

    apartments_to_csv(apart_path, apartments)
    stats_to_csv(stats_path, apartments)
    check_stats_change(stats_path)


if __name__ == '__main__':
    main()
