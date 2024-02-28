from backend.config import *
from backend.tests.db import db, app
from backend.authentication.user import User


class TestDatabase(unittest.TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app
        
    def setUp(self):
        with app.app_context():
            db.create_all()

        
    def test_users(self):
        with app.app_context():
            user1 = User(first_name='TEST', last_name="USER", email='alice@example.com', username=User().split_email('alice@example.com'), password='password', admin=User().is_admin('test', 'user', 'alice@example.com'))
            user2 = User(first_name='TEST', last_name="USER", email='bob@example.com', username=User().split_email('bob@example.com'), password='password', admin=User().is_admin('test', 'user', 'bob@example.com'))
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
        
        with app.app_context():
            users = User.query_all()
            self.assertEqual(len(users), 2)

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
