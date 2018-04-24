import logging
import re

import pandas as pd

import parser


def clean_data():
    # region private helper functions
    def load_data():
        south_list = pd.read_csv('../data/southbay.csv')
        south_data = pd.read_csv('../data/south-data.csv')
        north_list = pd.read_csv('../data/northbay.csv')
        north_data = pd.read_csv('../data/north-data.csv')
        return south_list, south_data, north_list, north_data

    def parse_bathroom(element):  # define shared bathroom as 0.5 ba
        return re.sub(r'shared', '0.5', element)

    def remove_null_sqft(element):
        return re.sub(r'available.*', '', element)

    def remove_letters(element):
        return re.sub(r'[a-zA-z]', '', element)

    def remove_units(element):
        return re.sub(r'(ft2|\$)', '', element)

    # endregion

    # region load and merge
    sl, sd, nl, nd = load_data()

    logging.debug(sl.columns)
    logging.debug(sd.columns)
    logging.debug(nl.columns)
    logging.debug(nd.columns)

    south = pd.merge(sl, sd, on='link')
    north = pd.merge(nl, nd, on='link')
    south['region'] = 0
    north['region'] = 1
    south = south.drop(columns=['Unnamed: 0_x'])
    north = north.drop(columns=['Unnamed: 0_x'])

    logging.debug(south.columns)
    logging.debug(north.columns)

    combined = south.merge(north)
    combined = parser.parse_housing(combined)  # TODO parse housing

    # endregion

