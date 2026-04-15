import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_redirect_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

if __name__ == "__main__":
    unittest.main()