# FraudDetector
Fraud detector endpoint for online advertising, submitted to Developer Week 2015 for the Virool Challenge

The rules for the challenge are here:

http://devweek.virool.com/rules

## Model Creation

We first extracted features using iPython, and generated test .CSV files to explore the data in Tableau

Once we had a set of about 15 features, we proceeded to create a Support Vector Machine model using Python scikit-learn, with a training set consisting on 80% of the data set, randomly selected.

## Endpoint Creation

To set up an endpoint capable of handling 1000 request per minute, we set up 16 Tornado processes with an Nginx load balancer upfront, using an Azure Ubuntu 8-core server

## Test

http://wwwhisper.cloudapp.net?ip=xxxx&user_agent=yyy&referer=zzz


