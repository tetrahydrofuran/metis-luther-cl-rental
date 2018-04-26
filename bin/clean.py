import logging
import re

import pandas as pd
import patsy


def clean_data():
    """
    Combines the Craigslist search results and details into a larger merged pandas DataFrame, which is
    exported to CSV
    Future extensibility would include option to not save, or rename destination
    :return: None
    """
    # region private helper functions
    def load_data():
        """
        Loads the four expected pandas DataFrames
        :return: Four pandas DataFrames, one for each saved CSV file
        """
        south_list = pd.read_csv('../data/southbay.csv')
        south_data = pd.read_csv('../data/south-data.csv')
        north_list = pd.read_csv('../data/northbay.csv')
        north_data = pd.read_csv('../data/north-data.csv')
        return south_list, south_data, north_list, north_data

    def parse_bathroom(element):  # define shared bathroom as 0.5 ba
        """Converts the 'shared' bathroom attribute to a 0.5 numeric"""
        return re.sub(r'shared', '0.5', element)

    def remove_null_sqft(element):
        """Non-reported sqft in detail extraction manifests as an 'available on...' field"""
        return re.sub(r'available.*', '', element)

    def remove_letters(element):
        """Remove letters, such as Bd/Ba to enable conversion of columns to numerics"""
        return re.sub(r'[a-zA-z]', '', element)

    def remove_units(element):
        """Removes units, specifically dollars and ft2 to enable conversion of columns to numerics"""
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


def prep_model(csv_name):
    """
    Loads CSV file of merged pandas DataFrame, cleans, converts categorical variable to a one-hot configuration
    Separates into dependent and independent features for regression
    :param csv_name: Name of CSV file to import, assumed to be in the ../data directory
    :return: x, y pandas DataFrames representing the features and dependent variable to perform regression upon
    """
    df = pd.read_csv('../data/' + csv_name)
    df = df.drop(columns=['Unnamed: 0', 'index', 'Unnamed: 0_y'], errors='ignore')
    housing_categorical = patsy.dmatrix('type', data=df, return_type='dataframe')
    df = df.join(housing_categorical)
    df = df.dropna()
    y = df['price']
    x = df.drop(columns=['price', 'type', 'hood', 'title', 'link'])
    return x, y


