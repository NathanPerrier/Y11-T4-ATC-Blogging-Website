from backend.config import *
from backend.db import *

class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('social.follower', lazy=True))  #social?
    
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    following = db.relationship('User', foreign_keys=[following_id], backref=db.backref('social.following', lazy=True)) #?social?
    
    @classmethod
    def get_all(cls, db):
        return db.session.query(cls).all()

    @classmethod
    def count_following(cls, db, user_id):
        return db.session.query(cls).filter_by(follower_id=user_id).count() #correct?
    
    @classmethod
    def count_followers(cls, db, user_id):
        return db.session.query(cls).filter_by(following_id=user_id).count()
    
    @classmethod
    def is_following(cls, db, follower_id, following_id):
        return db.session.query(cls).filter_by(follower_id=follower_id, following_id=following_id).count() > 0
    
    @classmethod
    def follow(cls, db, follower_id, following_id):
        if not cls.is_following(db, follower_id, following_id):
            db.session.add(cls(follower_id=follower_id, following_id=following_id))
            db.session.commit()
            return True
        return Social().unfollow(db, follower_id, following_id)
    
    @classmethod
    def unfollow(cls, db, follower_id, following_id):
        if cls.is_following(db, follower_id, following_id):
            db.session.query(cls).filter_by(follower_id=follower_id, following_id=following_id).delete()
            db.session.commit()
            return True
        return Social().follow(db, follower_id, following_id)
    
    @classmethod
    def delete_user(cls, db, user_id):
        try:
            db.session.query(cls).filter_by(follower_id=user_id).delete()
            db.session.query(cls).filter_by(following_id=user_id).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
