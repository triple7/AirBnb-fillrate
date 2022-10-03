from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests as R
from sqliteCommands import *
import argparse
import csv
import time

# BaseUrl where with baseUrl/[location]-[country]/ is the format
baseUrl = "https://www.airbnb.com.au"
# month conversion dictionary
MONTHS = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

def addLocation(location, country):
    location, country = location.lower(), country.lower()
    if not locationExists(location, country):
        insertLocation(location, country)
    else:
        print(f'Location {location} already exists')

def addLocationsFromCsv(filePath):
    with open(filePath, 'r') as file:
        entries = csv.reader(file, delimiter=',')
        count = 0
        for e in entries:
            count += 1
            addLocation(e[0], e[1])
    print(f'{count} locations added from csv. Exiting')

def addRooms(rooms):
    for r in rooms:
        if not roomExists(r):
            insertRoom(r)

def scrapeAvailabilities(location, locationUrl):
    page = R.get(locationUrl)
    soup = bs(page.content, "html.parser")
    rooms = [a for a in soup.find_all('a', href=True)]
    rooms = [a['href'] for a in rooms if 'rooms/' in a['href']]
    # Populate roomIds in db if new ones
    addRooms([int(r.split('/')[-1]) for r in rooms])

    # Now we got the results, parse each using selenium
# Change to chrome if preferred

    for i, r in enumerate(rooms):
        driver = webdriver.Safari()
        roomUrl = f'{baseUrl}{r}'
        roomId = r.split('/')[-1]
        driver.get(roomUrl)
        time.sleep(10)
        # Dig into the dom elements until reaching the cells
        calendar = driver.find_element(By.CSS_SELECTOR, "[aria-label=Calendar]")
        calendarGrid = calendar.find_elements(By.XPATH, "./child::*")[1]
        tableArea = calendarGrid.find_elements(By.XPATH, "./child::*")[0]
        cells = tableArea.find_elements(By.TAG_NAME, "td")
        
        availabilities = {}
        print(f'{len(cells)} for {roomId}')
        for c in cells:
            src = str(c.get_attribute('outerHTML'))
            if 'aria-label' in src:
                data = c.get_attribute('aria-label')
                if 'Available' not in data and 'Unavailable' not in data:
                    continue
                data = data.split(' ')
                day = data[0].replace(',', '')
                day = f'0{day}' if len(day) == 1 else day
                month = MONTHS[data[2].lower()]
                month = f'0{month} if len(month) == 1 else month'
                year = data[3].replace('.', '')
                formatDate = f'{year}-{month}-{day}'
                avail = data[4].lower()
                availabilities[formatDate] = avail
        
        # Finally update the availabilities for the room
        for t in availabilities:
            insertAvailability(roomId, t, availabilities[t])
        driver.close()
    print(f'Completed data scraping for location {location}')

def scrapeLocations():
    locations = selectLocations()
    for l in locations:
        location = l[0]
        country = l[1]
        url = f'{baseUrl}/{location}-{country}/stays'
        scrapeAvailabilities(location, url)
    print('All locations scraped. Exiting')

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('option', help='the function to operate[s=scrape all, *.csv=filepath of csv to add locations from]' )
    return parser

if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()
    
    if 'csv' in args.option:
        addLocationsFromCsv(args.option)
        exit()
    scrapeLocations()