from backend.config import *
from backend.db import *

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoriers = db.Column(db.String(50), nullable=False)
    
    @classmethod
    def get_by_id(cls, db, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def get_by_categories(cls, db, categories):
        return db.session.query(cls).filter_by(categories=categories).first()
    
    @classmethod
    def get_all(cls, db):
        return db.session.query(cls).all()
    
    @classmethod
    def add_categories(cls, db, categories):
        categories = cls(categories=categories)
        db.session.add(categories)
        db.session.commit()
        
    @classmethod
    def remove_categories(cls, db, id):
        categories = cls.get_by_id(db, id)
        db.session.delete(categories)
        db.session.commit()
        
    
        