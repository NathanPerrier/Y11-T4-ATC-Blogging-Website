from backend.config import *
from backend.forms.__init__ import *
from backend.data.address import Address
from backend.data.user_bio import Bio
from backend.social.social import Social
from backend.blog.blog import Blog
from backend.ai.image_generation import ImageGeneration 
from backend.db import *


FILE_PATH = r'frontend/static/images/user-images/avatars/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    first_name = db.Column(db.String(100), nullable=False) 
    last_name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100))
    
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)
    address = relationship('Address', backref=db.backref('user', lazy=True))
    
    bio_id = db.Column(db.Integer, db.ForeignKey('bio.id'), nullable=True)
    bio = relationship('Bio', backref=db.backref('user', lazy=True))
    
    avatar = db.Column(db.String(300), nullable=False)
    
    phone_number = db.Column(db.String(20), nullable=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    # social = relationship('Social', backref=db.backref('social', lazy=True))
    
    @classmethod
    def new(cls, db, *args, **kwargs):
        user = cls(*args, **kwargs)  
        db.session.add(user)  
        return user

    @classmethod
    def commit(cls, db):
        db.session.commit() 
        
    @classmethod
    def get_by_id(cls, db, id):
        return db.session.query(cls).filter_by(id=id).first()
              
    @classmethod
    def get_by_email(cls, db, email):
        return db.session.query(cls).filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, db, username):
        return db.session.query(cls).filter_by(username=username).first()
    
    @classmethod
    def get_all(cls, db):
        return db.session.query(cls).all()
    
    @classmethod
    def check_password(cls, user_password, password):
        return check_password_hash(user_password, password)
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def delete_user(self, db, user_id):      #?  issue when user deleted?    
        user = User().get_by_id(db, user_id)
        if user:  
            success = Address().delete_by_id(db, user.address_id)
            success = Bio().delete_by_id(db, user.bio_id)
            success = Social().delete_user(db, user.id)
            success = Blog().delete_blogs_by_user_id(db, user.id)
            db.session.delete(user) 
            db.session.commit() 
            print("User with id {} deleted.".format(user_id))
        else:
            print("User with id {} not found.".format(user_id))
    
    def login(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.get_user((form.email.data).lower())
            if user is not None:
                if User.check_password(user.password, form.password.data):
                    login_user(user, remember=True)
                    return ''
                return 'Invalid Password'
            return 'User Not Found'
        return 'Invalid Login Credentials'
        
    @classmethod    
    def signup(cls, first_name, last_name, email, password):
        user = cls(first_name=first_name.title(), last_name=last_name.title(), email=email.lower(), username=cls.split_email(email.lower()), password=password, avatar=('https://api.dicebear.com/6.x/initials/svg?seed='+first_name.title()+'&randomizeIds=true'), admin=cls.is_admin(first_name, last_name, email))
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            cls.send_welcome_email(first_name, email)
        except Exception as e:
            db.session.rollback()
            return False, 'Sever Error'
        finally:
            login_user(user, remember=True)
            return True, None
        
    @classmethod    
    def add_user(cls, first_name, last_name, email, password):
        user = cls(first_name=first_name.title(), last_name=last_name.title(), email=email.lower(), username=cls.split_email(email.lower()), password=password, avatar=('https://api.dicebear.com/6.x/initials/svg?seed='+first_name.title()+'&randomizeIds=true'), admin=cls.is_admin(first_name, last_name, email))
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        
    
    @classmethod
    def change_password(cls, email, new_password):  
        try:
            user = cls.get_by_email(db, email)
            if cls.check_password(user.password, new_password) == False:
                user.set_password(new_password)
                db.session.commit()
                return True, ''  #? True, None
            return False, "New password cannot be the same as the old password"
        except Exception as e:
            print(e)
            return False, 'Error changing password'
    
    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)
    
    def has_non_digit(self, inputString):
        return any(not char.isdigit() for char in inputString)
    
    @classmethod
    def update_account(cls, user, first_name, last_name, email, username, phone_number=None, street_number=None, street_name=None, suburb=None, postcode=None, bio=None):
        if (cls.get_by_email(db, email) is None and cls.get_by_email(db, email) != user) or cls.get_by_email(db, email) == user:
            if (cls.get_by_username(db, username) is None and cls.get_by_username(db, username) != user) or cls.get_by_username(db, username) == user:
                # if gmaps.geocode(address)[0]['formatted_address']:
                #     if (len(phone_number) == 10) and (cls.has_non_digit(phone_number) == False):
                #         if len(bio) <= 300:
                user.first_name = first_name.title()
                user.last_name = last_name.title()
                user.email = email.lower()
                user.username = username.lower()
                user.phone_number = phone_number
                if user.address is not None: Address().update(db, user.address, street_number, street_name, suburb, postcode)
                else: user.address = Address().add(db, street_number, street_name, suburb, postcode)
                if user.bio is not None: Bio().update(user.bio, bio)
                else: user.bio = Bio().add(bio=bio)
                db.session.commit()
                return ''
                #         return 'Bio must be less than 300 characters'
                #     return 'Invalid Phone Number'
                # return 'Invalid Address'
            return 'Username already in use'
        return 'Email already in use'
    
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
        
    @classmethod
    def is_admin(cls, first_name, last_name, email):
        pattern = r'^' + re.escape(last_name.lower() + first_name[0].lower()) + r'@atc\.qld\.edu\.au$'

        if not re.match(pattern, email):
            return False
        return True
    
    @classmethod
    def split_email(cls, email):
        username, domain = email.split('@')
        username= cls.check_username(username)
        return username

    @classmethod
    def check_username(cls, username):
        if cls.get_by_username(db, username) is not None:
            return cls.check_username(username + str(random.randint(10, 999)))
        return username
    
    @classmethod
    def get_user(cls, email):
        return User.get_by_email(db, email) if User.get_by_email(db, email) is not None else User.get_by_username(db, email)

    @classmethod
    def send_welcome_email(cls, first_name, email):
        send_email('contact.webgenieai@gmail.com', email, create_email(first_name, email, 'Welcome To The ATC Community!', 'Your account has been created! You can now post blogs and comment on other blogs!'))
     
     
    @classmethod
    def save_user_avatar(cls, user, image, AIcheckbox):
        try:
            if AIcheckbox:
                user.avatar = ImageGeneration().get_ai_avatar(str(user.first_name.title()))
            elif image and AIcheckbox == False:
                user.avatar = User().save_image(image)
            else:
                return True, ''
        except Exception as e:
            print(e)
            return False, 'Error saving image'
        finally:
            db.session.commit()
            return True, ''
        
    @classmethod
    def save_image(cls, img_file):
        try:
            directory = User().check_dir(FILE_PATH + User().generate_name() + '.png')
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
    
    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @classmethod
    def restore_user_avatar(cls, user):
        user.avatar = 'https://api.dicebear.com/6.x/initials/svg?seed='+user.first_name.title()+'&randomizeIds=true'
        db.session.commit()
        
    @login_manager.user_loader 
    def load_user(user):
        return User.query.get(int(user))

