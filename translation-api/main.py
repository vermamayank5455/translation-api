import unittest
from unittest.mock import patch
from flask import Flask, request, jsonify
import requests, json
import os
import redis
from dotenv import load_dotenv
import os

load_dotenv()

# importing values from env file
translator_api_key = os.environ.get('TRANSLATOR_API_KEY')
api_region = os.environ.get('TRANSLATOR_API_REGION')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')

redis_client = redis.Redis(host=redis_host, port=redis_port)


app = Flask(__name__)


@app.route('/translate', methods=['GET'])
def translate_text():
    # getting value passed through paramters
    text = request.args.get('text')
    source_lang = request.args.get('source_lang')
    target_lang = request.args.get('target_lang')

    # creating cache_key using paramters to store in redis
    cache_key = f'{source_lang}_{target_lang}_{text}'
    cached_translation = redis_client.get(cache_key)

    # if the request is already cached then then returning the response and not running further code
    if cached_translation is not None:
        return cached_translation


    # sending request to translation API from Bing
    api_url = 'https://api.cognitive.microsofttranslator.com/translate'
    headers = {'Ocp-Apim-Subscription-Key': translator_api_key,
               'Ocp-Apim-Subscription-Region': api_region,
               'Content-Type': 'application/json'}
    params = {'api-version': '3.0',
              'from': source_lang,
              'to': target_lang}
    body = [{'text': text}]
    response = requests.post(api_url, headers=headers, params=params, json=body)

    # if request fails returning a message
    if response.status_code != 200:
        return jsonify({'error': 'Translation failed'}), 400

    translation = response.json()[0]['translations'][0]['text']
    
    # storing cache in redis
    redis_client.set(cache_key, json.dumps({'translation': translation}))
    return jsonify({'translation': translation})



if __name__ == '__main__':
    app.run()
