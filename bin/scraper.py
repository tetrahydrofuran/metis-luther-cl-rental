import logging
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

import parser

RESULTS_PER_PAGE = 120


def pause():
    """
    Sleeps thread following a log-normal distribution
    :return: None
    """
    wait = np.random.lognormal(2, 0.5)
    logging.debug('Waiting ' + str(wait) + 's')
    time.sleep(wait)

# region Scraping search page
def scrape_apts(entries, url):
    """
    Scrapes multiple search pages of Craigslist apartments
    :param entries: Integer number of entries to scrape
    :param url: String of base URL of search page
    :return: pandas DataFrame containing the title, link, neighborhood, and price of each housing listing
    """
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
    listings.columns = ['title', 'link', 'hood', 'price']
    return listings


def scrape_apt_results_page(listings, url):
    """
    Scrapes each individual search result page
    :param listings: Dictionary of search entries and information
    :param url: String link of page to be scraped
    :return: listings input parameter with extra key and information extracted from param url
    """
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
def scrape_individual_listings(links):
    """
    Access point for scraping of individual listing detail pages
    :param links: Series of links of Craigslist entries to be scraped
    :return: pandas DataFrame of search results
    """
    result_dict = {}

    # region helper function definitions
    def listing_extraction(url):
        """
        Appends information from listing to growing results dictionary
        :param url: String of website URL to be scraped
        :return: Dictionary with appended key and information
        """
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
