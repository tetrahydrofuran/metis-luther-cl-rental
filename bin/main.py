import scraper
import export
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

# region SETTINGS
SAVE_INTERMEDIATES_DF = True
START_POINT = 1  # Document which dataframe to start from
url = 'https://sfbay.craigslist.org/search/sby/apa'
# endregion

# listings = scraper.scrape_apts(600, url)
# listings.to_csv('southbay.csv')

links = pd.read_csv('../bin/southbay.csv')
links.columns = ['title', 'link', 'hood', 'price']
logging.debug(links['link'].head())



# TODO check posting title for things like pool, etc.

