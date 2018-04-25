import logging
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

import parser

RESULTS_PER_PAGE = 120


def pause():
    # Please don't IP-ban me safeguard
    wait = np.random.lognormal(2, 0.5)
    logging.debug('Waiting ' + str(wait) + 's')
    time.sleep(wait)

# region Scraping search page
def scrape_apts(entries, url):
    listings = {}
    pages_to_scrape = entries // RESULTS_PER_PAGE
    if pages_to_scrape == 0:
        pages_to_scrape = 1
    logging.info('Scraping ' + str(pages_to_scrape) + ' pages')
    for i in range(pages_to_scrape):
        pause()
        scrape_url = url + '?s=' + str(i * RESULTS_PER_PAGE)
        listings = scrape_apt_results_page(listings, scrape_url)
    listings = pd.DataFrame.from_dict(listings, orient='index').reset_index()
    listings.columns = ['title', 'link', 'hood', 'price']  # TODO Verify
    return listings


# Scrapes individual search pages
def scrape_apt_results_page(listings, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    result_list = soup.find_all('p', class_='result-info')
    logging.debug(result_list)
    for result in result_list:
        listing = []  # [Link, Neighborhood, Price]
        link = result.find('a')
        listing.append(link['href'])
        try:
            listing.append(result.find('span', class_='result-hood').text.strip())
        except AttributeError:
            listing.append('')
        try:
            listing.append(result.find('span', class_='result-price').text.strip())
        except AttributeError:
            listing.append('')
        # logging.debug(listing)
        listings[link.text.strip()] = listing
    return listings
# endregion


# region Individual page scrape
# I know lexical scoping can be a bit iffy, but it seemed best here
def scrape_individual_listings(links):
    result_dict = {}

    # region helper function definitions
    def listing_extraction(url):
        logging.debug('listing_extraction(url)')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        listing = parser.parse_listing(soup)
        listing['link'] = url

        return listing
    # endregion

    for link in links:
        pause()
        try:
            result_dict[link] = listing_extraction(link)
            logging.debug(result_dict)
        except:
            # IndexError?
            # Dead link
            continue
    return pd.DataFrame.from_dict(result_dict, orient='index')

# endregion
