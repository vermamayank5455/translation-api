# translation-api


Translation API with Caching
This project implements a RESTful API that translates text using the Microsoft Translator Text API. The API also includes caching of translations to minimize API requests.

Requirements
Python 3.6 or higher
Flask
Redis
Requests
Python-dotenv
Installation
Clone this repository: git clone https://github.com/vermamayank5455/translation-api.git
Navigate into the project directory: cd translation-api
Install the required dependencies: pip install -r requirements.txt
Create a .env file in the project root directory and add the following environment variables with your own values:
makefile
Copy code
TRANSLATOR_API_KEY=<your_api_key>
TRANSLATOR_API_REGION=<your_api_region>
Start the Redis server on port 6379 (you can change this in app.py if needed).
Run the Flask application: python app.py
You can now access the API at http://localhost:5000/translate
API Usage
To translate text, make a GET request to /translate with the following query parameters:

text: The text to be translated.
source_lang (optional, default is "en"): The language code of the text to be translated.
target_lang (optional, default is "es"): The language code of the desired translation.
Example usage:

vbnet
Copy code
GET /translate?text=hello%20world&source_lang=en&target_lang=fr
This will translate the text "hello world" from English to French.

Caching
The API includes caching to minimize API requests. If a translation request has already been made for a particular text and language combination, the cached translation will be returned instead of making a new API request.

The cache is implemented using Redis. The cache key is constructed as follows: {source_lang}_{target_lang}_{text}. For example, the cache key for the text "hello world" translated from English to French would be "en_fr_hello world".

Testing
The project includes a set of test cases that can be run using unittest. To run the tests, navigate to the project directory and run:

Copy code
python -m unittest tests.test_translation_api
This will run the test cases in the test_translation_api.py file. The tests include checking that translations are returned correctly, that cached translations are returned instead of making new API requests, and that the cache is working as expected.

Limitations
This API is limited to 200,000 characters per month by the Microsoft Translator Text API. If you need to translate more text, you will need to upgrade your API subscription.
The caching system does not include a mechanism for expiring old cache entries, so the cache may continue to grow indefinitely. This could be addressed by adding a TTL (time to live) to each cache entry, or by periodically clearing the cache.
