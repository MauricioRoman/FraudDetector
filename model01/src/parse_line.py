#! /usr/bin/env python

from sklearn.externals import joblib
from common import extract_features_from_log, parse_log_line
import numpy as np
import sys

# Load the model and transformation objects
enc = joblib.load('../pickle/encoding01.pkl')
scaler = joblib.load('../pickle/scaler01.pkl')
clf = joblib.load('../pickle/model01.pkl')

def get_request():
    log_line = "  90.236.49.48    Mozilla%2F5.0+%28X11%3B+U%3B+Linux+i686%3B+en-US%3B+rv%3A1.8%29+Gecko%2F20051219+SeaMonkey%2F1.0b    http%3A%2F%2Ffaceboook.com "

    return log_line

def process_log_line(log_line):

    # Transform log line into a vector that can be fed into the model
    items = parse_log_line(log_line)
    features = np.array( extract_features_from_log(items, 'live_data') )
    encoded_features = enc.transform( features).toarray()
    scaled_features = scaler.transform(encoded_features)

    # Feed the vector to the model in order to get the prediction
    prediction = clf.predict(scaled_features)

    return prediction[0]

def main():

    log_line = get_request()
    prediction = process_log_line(log_line)

    if prediction == 0:
        print "403 Forbidden"
    elif prediction == 1:
        print "204 No content"


if __name__ == '__main__':
    sys.exit(main())