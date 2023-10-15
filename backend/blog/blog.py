from backend.config import *
from backend.db import *
from backend.blog.tags import Tags
from backend.blog.categories import Categories
from backend.blog.comments import Comments
from backend.blog.rating import Rating
from backend.ai.image_generation import ImageGeneration
from datetime import datetime


FILE_PATH = r'frontend/static/images/user-images/blogs/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=db.backref('blog', lazy=True))
    
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False) #workss? db.Text
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()) 
    image = db.Column(db.String(400), nullable=False) #default=ImageGeneration.get_ai_image(description)
    
    # tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=True)
    # tags = relationship('Tags', backref=db.backref('blog', lazy=True))
    
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)   
    categories = relationship('Categories', backref=db.backref('blog', lazy=True))
    
    
    @classmethod
    def get_by_id(cls, db, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def get_by_title(cls, db, title):
        return db.session.query(cls).filter_by(title=title).first()
    
    @classmethod
    def get_by_user_id(cls, db, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_date_posted(cls, db, date_posted):
        return db.session.query(cls).filter_by(date_posted=date_posted).all()
    
    @classmethod
    def get_by_tags_id(cls, db, tags_id):
        return db.session.query(cls).filter_by(tags_id=tags_id).all()
    
    @classmethod
    def get_by_categories_id(cls, db, categories_id):
        return db.session.query(cls).filter_by(categories_id=categories_id).all()
    
    @classmethod
    def get_all(cls, db):
        return db.session.query(cls).all()

    
    # @classmethod
    # def get_top_5(cls, db):
    #     return db.session.query(cls).order_by((cls.views).desc(), (cls.likes).desc(), (cls.dislikes).asc()).limit(5).all()
    
    @classmethod
    def create_blog(cls, db, user_id, title, description, content, image=None):  #check if user supplied image
        try: 
            image = ImageGeneration().get_ai_image(description) if image is None else cls.save_image(image, description)
            blog = cls(user_id=user_id, title=title, description=description, content=content, image=image)
            db.session.add(blog)
            db.session.commit()
            return True, '', blog.id
        except Exception as e:
            return False, str(e), ''
        
        

    @classmethod
    def edit_blog(cls, db, id, title, description, content, image):
        try:
            blog = cls.get_by_id(db, id)
            blog.title = title
            blog.description = description
            blog.content = content
            blog.image = image
            db.session.commit()
            return True, ''
        except Exception as e:
            return False, str(e)
            
    
    @classmethod
    def delete_blog(cls, db, id):
        try:
            blog = Blog().get_by_id(db, id)
            success = Comments().delete_by_blog_id(db, id)
            success = Rating().delete_by_blog_id(db, id)
            db.session.delete(blog)
            db.session.commit()
            return True, ''
        except Exception as e:
            print(e)
            return False, 'Database Error'
        
    @classmethod
    def delete_blogs_by_user_id(cls, db, user_id):
        try:
            blogs = cls.get_by_user_id(db, user_id)
            for blog in blogs:
                cls.delete_blog(db, blog.id)
            db.session.commit()
            return True
        except Exception as e:
            return False
    
    @classmethod
    def save_image(cls, img_file, description):
        try:
            directory = Blog().check_dir(FILE_PATH + Blog().generate_name() + '.png')
            img_file.save(os.path.join(FILE_PATH, directory.split(FILE_PATH)[1]))
            return directory
        except Exception as e:
            print(e)
        
        
    def generate_name(self, length=50):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def check_dir(self, directory):
        if os.path.exists(directory): #works?
            return self.check_dir(FILE_PATH + self.generate_name() + '.png')
        return directory
    
    # def change_image(self, image):
    #     if Blog().allowed_file(image):
    #         self.image = self.save_image(image, self.description)
    #         db.session.commit()
    #         return True
    #     return False
    
    
    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

