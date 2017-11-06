#!/usr/bin/env python

import dotenv
import os
import requests
from flask import Flask, request

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
verification_token = os.environ['VERIFICATION_TOKEN'].split(',')


@app.route('/apps/slack-latex', methods=['POST'])
def latex():
    if request.form['token'] in verification_token:
        query = request.form['text']
        r = requests.head('https://latex.codecogs.com/png.latex?' + query)
        if r.status_code == requests.codes.ok:
            response_url = request.form['response_url']
            payload_ack = {'response_type': 'ephemeral', 'text': query}
            r_ack = requests.post(response_url, json=payload_ack)
            payload_delayed = {'response_type': 'in_channel', 'attachments': [{'image_url': r.url, 'fallback': query}]}
            r_delayed = requests.post(response_url, json=payload_delayed)
            return '', 200


if __name__ == '__main__':
    app.run()
