from backend.config import *
from backend.db import db

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)

    
    @classmethod
    def get_by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def get_by_email(cls, email):
        return db.session.query(cls).filter_by(email=email).first()
    
    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()
    
    @classmethod
    def add_user_to_newsletter(cls, db, email):
        if cls.get_by_email(email):
            return False, 'Email already Subscribed'
        newsletter = cls(email=email)
        db.session.add(newsletter)
        db.session.commit()
        return True, None
        
    @classmethod
    def remove_user_from_newsletter(cls, email):
        newsletter = cls.get_by_email(email)
        db.session.delete(newsletter)
        db.session.commit()
        
 