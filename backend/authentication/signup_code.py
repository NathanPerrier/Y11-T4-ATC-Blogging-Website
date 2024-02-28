from datetime import datetime, timedelta
from backend.config import *
from backend.forms.__init__ import create_email, send_email 
from backend.authentication.user import User
from backend.db import *


class SignupCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(100), nullable=False)
    reset_code = db.Column(db.String(6), nullable=False) 
    
    expiration_time = db.Column(db.DateTime, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)

    @classmethod
    def check_email(cls, email):
        """Check if the email is in the database."""
        return db.session.query(User).filter_by(email=email).first()    
    
    @classmethod
    def is_name_valid(cls, name):
        """Check if the name if valid"""
        valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"    
        for char in name:
            if char not in valid_chars:
                return False 
        return True


    def generate_code(length=6):
        """Generate a random numerical reset code of the given length."""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length)) 

    @staticmethod
    def send_reset_code(first_name, email, code):
        """Send the reset code to the user's email."""
        try:
            send_email('contact.webgenieai@gmail.com', email, create_email(first_name, email, 'Verification Code', code))
        except Exception as e:
            print(e)

    @classmethod
    def store_reset_code(cls, email, code, expiration_duration=1800): # 30 mins
        """Store the reset code in the database with an expiration time."""
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration_duration)
        reset_entry = SignupCode(email=email, reset_code=generate_password_hash(code), expiration_time=expiration_time, creation_time=datetime.utcnow())
        db.session.add(reset_entry)
        db.session.commit()

    @classmethod
    def create_and_send_reset_code(cls, first_name, last_name, email):
        """Generate, send, and store the reset code."""
        if cls.check_email(email) is None:
            if cls.is_name_valid(first_name) and cls.is_name_valid(last_name):
                if cls.check_email_format(email):
                    if cls.check_active_code(email):
                        code = cls.generate_code()
                        cls.send_reset_code(first_name, email, code)
                        cls.store_reset_code(email, code) 
                        return True, None
                    return True, None #has active code (continue)
                return False, 'Invalid Email Format'
            return False, 'Invalid Name(s)'
        return False, "Email Already Registered"
    
    @classmethod
    def check_email_format(cls, email):
        try:
            username, domain = email.split('@')
            domain, tld = domain.rsplit('.', 1)
            return True
        except ValueError:
            return False

        
    @classmethod
    def check_active_code(cls, email):
        if db.session.query(cls).filter_by(email=email).filter(SignupCode.expiration_time > datetime.utcnow()).first():
            return False
        return True
    
    @classmethod
    def check_code(cls, user_code, code):
        return check_password_hash(user_code, code)
    
    @classmethod    
    def check_reset_code(cls, email, input_code):
        reset_entry = db.session.query(cls).filter_by(email=email).order_by(SignupCode.creation_time.desc()).first()
    
        if not reset_entry:
            return False, "No reset code found for the user"

        if cls.check_code(reset_entry.reset_code, input_code) == False:
            print(reset_entry.reset_code, input_code)
            return False, "Invalid reset code"

        current_time = datetime.utcnow()
        if current_time > reset_entry.expiration_time:
            return False, "Reset code has expired"

        return True, None
    