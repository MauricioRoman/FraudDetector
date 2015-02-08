#! /usr/bin/env python

import sys


def main():

    f = open('../data/train_data.tsv')
    data = []
    for line in f:
        line_array = line.split('\t')
        status = line_array[3]
        arguments = line_array[0:3]
        if status == 'true\n':
            data.append(arguments)

    f = open('../data/webapp_test_data.txt', 'w')
    f.write("[\n")
    for item in data:
        f.write("%s,\n" % item)
    f.write("]\n")

if __name__ == '__main__':
    sys.exit(main())