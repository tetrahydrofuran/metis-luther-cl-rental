import scraper
import export
import logging
import pandas as pd
import os
import clean

logging.basicConfig(level=logging.DEBUG)

# region SETTINGS
CONTINUE_FROM_INTERMEDIATE = True
RESCRAPE = False
ROWS_TO_SCRAPE = 600
sb_url = 'https://sfbay.craigslist.org/search/sby/apa'
nb_url = 'https://sfbay.craigslist.org/search/nby/apa'
# endregion

# if not os.path.isfile('../data/northbay.csv') or not os.path.isfile('../data/southbay.csv'):
#     southbay = scraper.scrape_apts(ROWS_TO_SCRAPE, sb_url)
#     northbay = scraper.scrape_apts(ROWS_TO_SCRAPE, nb_url)
#     southbay.to_csv('../data/southbay.csv')
#     northbay.to_csv('../data/northbay.csv')

clean.clean_data()
#
# links = pd.read_csv('../bin/northbay.csv')
# #links.columns = ['title', 'link', 'hood', 'price']
# logging.debug(links['link'].head())
#
# data_i_hope_this_works = scraper.scrape_individual_listings(links['link'])
#
# data_i_hope_this_works.to_csv('north-details.csv')
# TODO check posting title for things like pool, etc.
# TODO distance from san francisco?
# https://www.propertyshark.com/Real-Estate-Reports/most-expensive-zip-codes-in-the-us

