from backend.config import *
from backend.db import *
from datetime import datetime

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    relates_to_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    relates_to = db.relationship('Comments', backref=db.backref('comments', lazy=True), remote_side='Comments.id')
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    blog = db.relationship('Blog', backref=db.backref('comments', lazy=True))
    
    comment = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_by_id(cls, db, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def get_by_user_id(cls, db, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_blog_id(cls, db, blog_id):
        return db.session.query(cls).filter_by(blog_id=blog_id).order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def get_by_user_and_blog_id(cls, db, user_id, blog_id):
        return db.session.query(cls).filter_by(user_id=user_id, blog_id=blog_id).all()
    
    @classmethod
    def get_by_blog_id_related(cls, db, blog_id):
        return db.session.query(cls).filter((cls.blog_id == blog_id) & (cls.relates_to_id.isnot(None))).all()
    
    @classmethod
    def get_by_relates_to(cls, db, comment_id):
        return db.session.query(cls).filter_by(relates_to_id=comment_id).all()
    
    @classmethod
    def add_comment(cls, db, user_id, blog_id, comment):
        comment = cls(user_id=user_id, blog_id=blog_id, comment=comment)
        db.session.add(comment)
        db.session.commit()
    
    @classmethod
    def delete_by_blog_id(cls, db, blog_id):
        comments = cls.get_by_blog_id(db, blog_id)
        for comment in comments:
            cls.delete_comment(db, comment.id)    
        db.session.commit()
        return True 
    
    @classmethod
    def delete_comment(cls, db, id):
        comment = cls.get_by_id(db, id)
        relates_to_comments = cls.get_by_relates_to(db, id)
        for _comment_ in relates_to_comments:
            cls.delete_comment(db, _comment_.id)
        db.session.delete(comment)
        db.session.commit()
    
    @classmethod
    def edit_comment(cls, db, id, comment_edit):
        comment = cls.get_by_id(db, id)
        comment.comment = comment_edit
        db.session.commit()
        
    @classmethod
    def reply_to_comment(cls, db, comment_id, user_id, blog_id, comment):
        comment = cls(relates_to_id=comment_id, user_id=user_id, blog_id=blog_id, comment=comment)
        db.session.add(comment)
        db.session.commit()
