import pickle
import pandas as pd


# Load pickle into data structure
def pickler(pkl):
    with open(pkl, 'rb') as f:
        struc = pickle.load(f)
        f.close()
    return struc


def picklew(struc, pkl):
    with open(pkl, 'wb') as f:
        pickle.dump(struc, pkl)
        f.close()


def dump_pd(df, name):
    picklew(df, name + '.pkl')
    df.to_csv(name + '.csv')
