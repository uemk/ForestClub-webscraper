# ForestClub Web Scraper
Apartments web scraper: https://www.forestclub.com.pl/

## Description
ForestClub is a python program, written for purely PERSONAL NEEDS, 
to automate tracking the changes in the following residential investment website: 
https://www.forestclub.com.pl/wyszukaj/?flat-type=Mieszkanie&area=&room=&floor=#flats-list.

NOTE: the script aims to be used for several months from the date of creation 
(as some updates are planned in this period) and its main goal is to send 
the notification once the new apartments appear on the website for sale.
   
##  How it works?
* scraps and parses a given site using selenium and Beautiful Soup
* saves all found apartments in apartments.csv
(if file exists it is overwritten)
* saves statistics concerning number of total/free/sold apartments to stats.csv 
(if file exists new stats are appended)
* in case new statistics are different than previous ones 
a proper notification e-mail is generated and sent using Gmail API
* launching the script should be triggered automatically 
(e.g. daily or after each reboot or ...) via cron configuration 
or other workflow manager 

## Usage

TODO

## Requirements

Needed libraries are listed in requirements.txt file
