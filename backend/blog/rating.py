from backend.config import *
from backend.db import *
import math


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=db.backref('rating', lazy=True))
    
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    blog = relationship('Blog', backref=db.backref('rating', lazy=True))

    rating = db.Column(db.Boolean, nullable=False) #good?
    
    @classmethod
    def get_by_id(cls, db, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def count_likes(cls, db, blog_id):
        return db.session.query(cls).filter_by(blog_id=blog_id, rating=True).count()
    
    @classmethod
    def count_dislikes(cls, db, blog_id):
        return db.session.query(cls).filter_by(blog_id=blog_id, rating=False).count()
    
    @classmethod
    def get_all(cls, db):
        return db.session.query(cls).all()
    
    @classmethod
    def get_by_blog_and_user_id(cls, db, blog_id, user_id):
        return db.session.query(cls).filter_by(blog_id=blog_id, user_id=user_id).first()
    
    @classmethod
    def get_by_user_id(cls, db, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_blog_id(cls, db, blog_id):
        return db.session.query(cls).filter_by(blog_id=blog_id).all()
    
    @classmethod
    def add_rating(cls, db, blog_id, rating):
        print('add rating')
        if cls.get_by_blog_and_user_id(db, blog_id, current_user.id):
            print('change rating')
            cls.change_rating(db, blog_id, rating)
        else:
            rating = cls(user_id=current_user.id, blog_id=blog_id, rating=rating)
            db.session.add(rating)
            db.session.commit()
    
    @classmethod
    def delete_by_blog_id(cls, db, blog_id):
        ratings = cls.get_by_blog_id(db, blog_id)
        for rating in ratings:
            cls.delete_rating(db, rating.id)  
        db.session.commit()
        return True  
        
    @classmethod
    def delete_rating(cls, db, id):
        rating = cls.get_by_id(db, id)
        db.session.delete(rating)
        db.session.commit()
    
    @classmethod
    def change_rating(cls, db, blog_id, rating):
        _rating_ = cls.get_by_blog_and_user_id(db, blog_id, current_user.id)
        if _rating_.rating == rating:
            cls.delete_rating(db, _rating_.id)
        else:
            _rating_.rating = rating
            db.session.commit()
        
    @classmethod
    def get_featured_blogs(cls, db, blog_object):
        ratings = Rating().get_all(db)
        print('ratings:', ratings)
        
        # Create dictionaries to store the total likes and dislikes for each blog
        blog_likes = {}
        blog_dislikes = {}

        # Calculate total likes and dislikes for each blog
        for rating in ratings:
            if rating.blog_id not in blog_likes:
                blog_likes[rating.blog_id] = 0
            if rating.blog_id not in blog_dislikes:
                blog_dislikes[rating.blog_id] = 0
            
            if rating.rating:
                blog_likes[rating.blog_id] += 1
            else:
                blog_dislikes[rating.blog_id] += 1
                
        
        # Calculate the blog ratings based on likes and dislikes for each blog
        for rating in ratings:
            total_likes = blog_likes[rating.blog_id]
            total_dislikes = blog_dislikes[rating.blog_id]

            rating.v = Rating().calculate_blog_rating(total_likes, total_dislikes)
            print('rating:', rating.v)
            
        # Sort the ratings
        sorted_ratings = sorted(ratings, key=lambda r: r.v, reverse=True)

        # Get the top 5 blog ids with the highest ratings
        top_blog_ids = [r.blog_id for r in sorted_ratings]
        top_blog_ids = top_blog_ids[:5]

        # Get the top 5 blogs with the highest ratings
        top_blogs = [blog_object.get_by_id(db, blog_id) for blog_id in top_blog_ids]

        return top_blogs
    

    def calculate_blog_rating(self, likes, dislikes):
       # Calculate the ratio of likes to total votes (likes + dislikes)
        total_votes = likes + dislikes
        
        activity_factor = 1 + min(1, total_votes / 50)
        print('factor:', activity_factor)
        
        ratio = (0 if total_votes == 0 or likes == 0 else likes / total_votes)
        
        # Map the ratio to the range [0, 2π] to use in the cosine function
        x = 2 * math.pi * ratio

        # Calculate the rating using the given function
        rating = ((2.5 * math.cos(x) + 2.5) if x>0 else 0) * activity_factor

        return round(min(5, max(0, rating)), 2)
            
