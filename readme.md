# AirBnb fillRateParser

# Introduction

This project takes air bnb data from across Australia, geo locates each room, parses its availabilities and provides statistical views of the data as a heat map.

Secondarily, the data is compared for analysis with real estate prices in the same areas to give some intuitionb on whether it is more affordable to invest in a place that can be managed using airBnb as the fill rate is high, and calculate the potential returns over time.

Finally, using data scraped from real estate sites, a comparative table of airbnb vs long term rent benefit analysis will be made.

# Dependencies

The following modules are required:
. 
# Usage

Fill out the locations.csv table with a 2 field entry:
. location: the name of a location ie: Brisbane 
. country

Once filled out, use the following command to enter the locations into the local database in ./db/db.sqlite3

python3 airBnbParser.py ./locations.csv

Once the database is populated, it's time to scrape the availability info with:

python3 airBnbParser.py s

This will go through each roomId found on each location page, and run a selenium GUI manipulation session.

Note: as this is a GUI manipulation method of scraping data, you're better off having a coffee until it's done.

