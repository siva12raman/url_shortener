import unittest
from app import app


class FlaskApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_ping(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'pong'})

    def test_create_short_url_success(self):
        payload = {'long_url': 'https://example.com/very-long-url', 'alias': 'my-link'}
        response = self.client.post('/api/v1/urls', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('short_url', data)
        self.assertIn('expires_at', data)
        self.assertIn('created_at', data)

    def test_create_short_url_invalid(self):
        response = self.client.post('/api/v1/urls', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'invalid URL'})


if __name__ == '__main__':
    unittest.main()
