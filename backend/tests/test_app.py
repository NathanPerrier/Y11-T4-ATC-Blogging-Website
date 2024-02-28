from backend.config import *
from backend.tests.db import db

class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        # initialize the flask app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def test_index(self):
        # test the index page
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Tracking App", response.data)

    def test_json_response(self):
        # test the json response
        response = self.client.get('/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, {'message': 'Hello, World!'})
        
    def test_404(self):
        # test the 404 page
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page not found", response.data)
    
    def test_500(self):
        # test the 500 page
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Internal server error", response.data)
    
    def test_login(self):
        # test the login page
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)
    
    def test_signup(self):
        # test the signup page
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)
