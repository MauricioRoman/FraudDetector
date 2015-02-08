#! /usr/bin/env python

from sklearn import svm
from pandas import read_csv
from pandas import DataFrame
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.externals import joblib
import sys

def main():

    # Read test and training data
    training = read_csv('../data/training.csv', index_col=0)
    test = read_csv('../data/test.csv', index_col=0)

    # Extract y-values from dataframe into numpy array
    y = training['status'].values
    y_test = test['status'].values

    # Drop y-column from dataframe
    training = training.drop(['status'], axis=1)
    test = test.drop(['status'], axis=1)

    # Extract X-matrix
    X = training.values
    X_test = test.values

    # Encode categorical data so that each category is its own feature, with boolean values
    indices_to_fit = range(11)
    enc = OneHotEncoder(categorical_features=indices_to_fit)
    enc.fit(X)

    X_hot_encoded = enc.transform(X).toarray()
    X_test_hot_encoded = enc.transform(X_test).toarray()

    # Normalize data to zero mean and unit standard deviation
    scaler = StandardScaler().fit(X_hot_encoded)
    X_scaled = scaler.transform(X_hot_encoded)
    X_test_scaled = scaler.transform(X_test_hot_encoded)

    # Fit a SVM model
    clf = svm.SVC()
    clf.fit(X_scaled,y)    #This costs about 3-5 seconds
    y_predicted = clf.predict(X_test_scaled)

    results = DataFrame([y_predicted, y_test]).T
    results.columns = ['predicted', 'actual']
    results['sum'] = results['predicted'] + results['actual'] # Add and substract
    print results.groupby('sum').count()
    results['sub'] = results['predicted'] - results['actual'] # Add and substract
    print results.groupby('sub').count()

    # Save the model into a pickle file
    joblib.dump(clf, '../pickle/model01.pkl')
    joblib.dump(enc, '../pickle/encoding01.pkl')
    joblib.dump(scaler, '../pickle/scaler01.pkl')

if __name__ == '__main__':
    sys.exit(main())