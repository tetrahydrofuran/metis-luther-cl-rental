import logging
import os

import clean
import model
import scraper

# region SETTINGS
ROWS_TO_SCRAPE = 600
sb_url = 'https://sfbay.craigslist.org/search/sby/apa'
nb_url = 'https://sfbay.craigslist.org/search/nby/apa'
# endregion

# Scrape Craigslist if scraped data is not present
if not os.path.isfile('../data/northbay.csv') or not os.path.isfile('../data/southbay.csv'):
    southbay = scraper.scrape_apts(ROWS_TO_SCRAPE, sb_url)
    northbay = scraper.scrape_apts(ROWS_TO_SCRAPE, nb_url)
    southbay.to_csv('../data/southbay.csv')
    northbay.to_csv('../data/northbay.csv')
if not os.path.isfile('../data/merge.csv'):
    clean.clean_data()

# Option to change to 'merge2.csv'
x, y = clean.prep_model('merge.csv')

# Fit model and generate plots
lm, selected_x = model.model(x, y)
model.plot_analyze(lm, selected_x, y)
