# From: backend/hosting/__init__.py
from backend.config import *
from backend.__init__ import *

def create_app():
    # Initialize app
    app = Flask(__name__, template_folder='../../frontend/templates/', static_folder='../../frontend/static/')
    
    # Configure app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = random.randbytes(32)
    app.config['BLOG_UPLOAD_FOLDER'] = 'frontend/static/images/user-images/blogs/'
    app.config['AVATAR_UPLOAD_FOLDER'] = 'frontend/static/images/user-images/avatars/'
    app.config['AI_UPLOAD_FOLDER'] = 'frontend/static/images/ai-images/blogs/'
    
    # Initialize extensions
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(sign_up)
    app.register_blueprint(terms)
    app.register_blueprint(blog)
    app.register_blueprint(subject)
    app.register_blueprint(forgot)
    app.register_blueprint(account)
    app.register_blueprint(admin)
    app.register_blueprint(tracking)  
    
    # Register error handlers
    register_error_handlers(app)
    
    # Initialize database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app



