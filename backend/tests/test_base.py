from backend.config import *
from backend.tests.db import db, app

class BaseTestCase(unittest.TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()