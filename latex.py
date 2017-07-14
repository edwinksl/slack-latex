#!/usr/bin/env python

import dotenv
import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
verification_token = os.environ['VERIFICATION_TOKEN']


@app.route('/latex', methods=['POST'])
def latex():
    if request.form['token'] == verification_token:
        query = request.form['text']
        r = requests.get('https://latex.codecogs.com/png.latex?' + query)
        if r.status_code == requests.codes.ok:
            payload = {'response_type': 'in_channel', 'attachments': [{'image_url': r.url}]}
            return jsonify(payload)


if __name__ == '__main__':
    app.run()
