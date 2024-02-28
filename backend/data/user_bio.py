from backend.config import *
from backend.db import *

class Bio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_bio = db.Column(db.String(300), nullable=False)
    
    @classmethod
    def add(cls, bio):
        bio = cls(user_bio=bio)
        db.session.add(bio)
        return bio
    
    @classmethod
    def get_by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, bio, user_bio):
        bio.user_bio = user_bio
        db.session.commit()
        
    @classmethod
    def delete_by_id(cls, db, id):
        try:
            bio = cls.get_by_id(id)
            db.session.delete(bio)
            db.session.commit()
            return True
        except Exception as e:
            return False