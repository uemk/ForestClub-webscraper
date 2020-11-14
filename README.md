# ForestClub Web Scraper
Apartments web scraper for the website: https://www.forestclub.com.pl/

#### Table of Contents
* [Description](#description)
* [How it works?](#how-it-works)
* [Usage](#usage)
    * [Files needed to run an application](#files-needed-to-run-the-application)
    * [Files generated by the application](#files-generated-by-the-application)
    * [Running the application](#running-the-application)
* [Requirements](#requirements)

## Description
ForestClub is a python program, written for PERSONAL needs, 
to automate tracking the changes in the following residential investment website: 
https://www.forestclub.com.pl/wyszukaj/?flat-type=Mieszkanie&area=&room=&floor=#flats-list.

NOTE: the script aims to be used for several months from the date of creation 
(as the new information should appear on the website in this timeframe) and its main goal is to send 
the notification once the new apartments appear on the website for sale.

##  How it works?
* scraps and parses a given site using selenium web-driver and Beautiful Soup
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
### Files needed to run the application:
* *forestclub.py* - main program (web scraper)
* *my_gmail.py* - module (imported by *forestclub.py*) implementing sending e-mails via Gmail API 
* *.env* - file holding information about sender and recipient e-mail addresses 
according to the format presented in *.env.example* template
* *credentials.json* - file with Gmail API credentials generated from personal project on Google platform, 
according to the format presented in *credential.json.example* template 

### Files generated by the application:
* *apartments.csv* - file with list of apartments found on the website
* *stats.csv* - file with statistics concerning apartments 
* *token.pickle* - file with saved credentials to access Gmail API

### Running the application:
* Linux shell:
    * add execute permission: chmod +x forestclub.py 
    * run: ./forestclub.py (or python3 forestclub.py)
    * schedule launching the script in cron according to the instructions in *crontab.example*

## Requirements
* python libraries/modules from *requirements.txt*
* create the project on Google Cloud Platform and enable Gmail API:
    *  then create credentials, download them and save as *credentials.json*
