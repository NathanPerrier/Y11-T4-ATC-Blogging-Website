from backend.config import *
from backend.db import *

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    
    @classmethod
    def get_by_id(cls, db, id):
        return db.session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_by_tag(cls, db, tag):
        return db.session.query(cls).filter_by(tag=tag).first()
    
    @classmethod
    def get_all(cls, db):
        return db.session.query(cls).all()
    
    @classmethod
    def add_tag(cls, db, tag):
        tag = cls(tag=tag)
        db.session.add(tag)
        db.session.commit()
        
    @classmethod
    def remove_tag(cls, db, id):
        tag = cls.get_by_id(db, id)
        db.session.delete(tag)
        db.session.commit()