import logging
import re
import patsy

import pandas as pd


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

    combined = south.append(north).reset_index()
    # region clean data
    combined['bed'] = pd.to_numeric(combined['bed'].apply(remove_letters))
    combined['bath'] = combined['bath'].apply(parse_bathroom)
    combined['bath'] = pd.to_numeric(combined['bath'].apply(remove_letters))
    combined['sqft'] = combined['sqft'].apply(remove_null_sqft)
    combined['sqft'] = pd.to_numeric(combined['sqft'].apply(remove_units))
    combined['price'] = pd.to_numeric(combined['price'].apply(remove_units))

    combined = combined.drop(columns=['index', 'Unnamed: 0_y'])
    combined = combined.dropna()
    # endregion

    logging.debug(combined.columns)
    combined.to_csv('../data/merge.csv')


def prep_model():
    df = pd.read_csv('../data/merge.csv')
    df = df.drop(columns=['Unnamed: 0', 'index', 'Unnamed: 0_y'], errors='ignore')
    housing_categorical = patsy.dmatrix('type', data=df, return_type='dataframe')
    df = df.join(housing_categorical)
    df = df.dropna()
    y = df['price']
    x = df.drop(columns=['price', 'type', 'hood', 'title', 'link'])
    return x, y


