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

data_i_hope_this_works = scraper.scrape_individual_listings(links['link'])

#output = scraper.scrape_individual_listings(['https://sfbay.craigslist.org/sby/apa/d/1500-off-on-this-wonderful/6568384604.html', 'https://sfbay.craigslist.org/sby/apa/d/spacious-and-immaculate/6568383937.html'])
data_i_hope_this_works.to_csv('testrun.csv')
# TODO check posting title for things like pool, etc.

