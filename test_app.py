import unittest
from app import app


class PingEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_ping(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'pong'})


if __name__ == '__main__':
    unittest.main()
