#! /usr/bin/env python

from sklearn.externals import joblib
from common import extract_features_from_log, parse_log_line
import numpy as np
import sys
import tornado.escape
import tornado.ioloop
import tornado.web
import argparse

# Load the model and transformation objects
enc = joblib.load('../pickle/encoding01.pkl')
scaler = joblib.load('../pickle/scaler01.pkl')
clf = joblib.load('../pickle/model01.pkl')

def process_arguments(args):

    parser = argparse.ArgumentParser(
        description="Tornado webapp to score bots")

    # Let's add our arguments
    parser.add_argument('--port',
                        dest='port',
                        type=int,
                        required=True,
                        help='Port number'
                        )
    options = parser.parse_args(args)

    return options

class LogHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        ip = self.get_argument('ip')
        user_agent = self.get_argument('user_agent')
        referer = self.get_argument('referer')
        items = [ip, user_agent, referer]

        try:
            features = np.array( extract_features_from_log(items, 'live_data') )
            encoded_features = enc.transform( features).toarray()
            scaled_features = scaler.transform(encoded_features)
            prediction = clf.predict(scaled_features)
            if prediction == 0:
                self.set_status(403)
                self.finish()
            elif prediction == 1:
                self.set_status(204)
                self.finish()

        except:
            self.set_status(403)
            self.finish()


application = tornado.web.Application([
    (r"/", LogHandler)
])


if __name__ == '__main__':
    options = process_arguments(sys.argv[1:])
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
