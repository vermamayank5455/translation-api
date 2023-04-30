import unittest
from unittest.mock import patch
import json
# importing app object and redis connection object from main.py
from main import app, redis_client


class TestTranslationAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        redis_client.flushdb()

    @patch('requests.get')
    def test_translation_api(self, mock_post):
        # setting param values
        source_lang = 'en'
        target_lang = 'fr'
        text = 'hello world'

        mock_post.return_value.json.return_value = [{'translations': [{'text': 'Bonjour le monde!'}]}]


        response = self.app.get(f'/translate?source_lang={source_lang}&target_lang={target_lang}&text={text}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['translation'], "Salut tout le monde")
        self.assertEqual(mock_post.call_count, 0)
        mock_post.reset_mock()

        # Cached transaction
        response = self.app.get(f'/translate?source_lang={source_lang}&target_lang={target_lang}&text={text}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['translation'], "Salut tout le monde")
        self.assertEqual(mock_post.call_count, 0)
        mock_post.reset_mock()


        text = 'How are you?'
        mock_post.return_value.json.return_value = [{'translations': [{'text': 'Comment ça va?'}]}]

        response = self.app.get(f'/translate?source_lang={source_lang}&target_lang={target_lang}&text={text}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['translation'], 'Comment vas-tu?')
        self.assertEqual(mock_post.call_count, 0)


if __name__ == '__main__':
    unittest.main()
