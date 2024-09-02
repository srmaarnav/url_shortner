import unittest
import json
from app import app, url_mapping  # Import the Flask app from app.py

class URLShortenerTests(unittest.TestCase):
    def setUp(self):
        """Set up the test client and other necessary configurations."""
        self.app = app.test_client()
        self.app.testing = True
        url_mapping.clear()

    def test_shorten_url(self):
        """Test the URL shortening functionality."""
        # Test shortening a new URL
        response = self.app.post('/shorten', 
            data=json.dumps({"long_url": "https://www.example.com"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('short_url', data)

        # Test shortening a URL that already exists
        response = self.app.post('/shorten', 
            data=json.dumps({"long_url": "https://www.example.com"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_shorten_url_invalid(self):
        """Test the URL shortening functionality with an invalid URL."""
        response = self.app.post('/shorten', 
            data=json.dumps({"long_url": "invalid-url"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid URL')

    
    def test_get_long_url(self):
        """Test retrieving the long URL from a short code."""
        # First, shorten a URL to get a short code
        response = self.app.post('/shorten', 
            data=json.dumps({"long_url": "https://www.example.com"}),
            content_type='application/json'
        )
        short_url = json.loads(response.data)['short_url']
        short_code = short_url.split('/')[-1]  # Extract the short code

        # Now, retrieve the long URL using the short code
        response = self.app.get(f'/{short_code}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['long_url'], "https://www.example.com")

    def test_get_non_existent_long_url(self):
        """Test retrieving a long URL that does not exist."""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_list_urls(self):
        """Test listing all stored URLs."""
        # Shorten a URL first
        self.app.post('/shorten', 
            data=json.dumps({"long_url": "https://www.example.com"}),
            content_type='application/json'
        )
        response = self.app.get('/urls')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)  # Ensure there is at least one URL

if __name__ == '__main__':
    unittest.main()