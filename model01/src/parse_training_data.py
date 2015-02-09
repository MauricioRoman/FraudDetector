#! /usr/bin/env python

from pandas import DataFrame, read_csv
import sys
import numpy as np
from common import extract_features_from_log


def main():

    f = open('../data/train_data.tsv')
    data = []
    for line in f:
        row = extract_features_from_log( line.split('\t'), 'training_data' )
        data.append(row )

    columns = ['ip_1', 'ip_2', 'ip_3', 'ip_4', 'category', 'os_version', 'version', 'vendor',
                  'name', 'os', 'scheme', 'hostname', 'alexa_top_million', 'len_path', 'len_query',
                  'len_host','status']

    df = DataFrame(data, columns = columns)

    # Write feature matrix
    df.to_csv('../data/features.csv')

    # Separate data into test and training sets
    mask = np.random.rand(len(df)) < 0.8
    train = df[mask]
    test = df[~mask]
    train.to_csv('../data/training.csv')
    test.to_csv('../data/test.csv')

if __name__ == '__main__':
    sys.exit(main())
