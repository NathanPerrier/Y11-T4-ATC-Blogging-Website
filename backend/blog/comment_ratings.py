from backend.config import *
from backend.db import *

class CommentLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    comment = db.relationship('Comments', backref=db.backref('comments', lazy=True))
    
    rating = db.Column(db.String(10), nullable=False)