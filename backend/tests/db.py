from backend.config import *
from backend.db import db

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = random.randbytes(32)

db.init_app(app)