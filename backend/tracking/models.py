from backend.db import db


class Site(db.Model):
    __tablename__ = 'tracking_site'

    id = db.Column(db.Integer, primary_key=True)
    base_url = db.Column(db.String)
    visits = db.relationship('Visit', backref='site', lazy='select')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def query_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_user(cls, user):
        return cls.query.filter_by(user_id=user.id).all()
    
    @classmethod
    def get_by_url(cls, url):
        return cls.query.filter_by(base_url=url).first()

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)
    
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def __repr__(self):
        return '<Site {:d} {}>'.format(self.id, self.base_url)

    def __str__(self):
        return self.base_url


class Visit(db.Model):
    __tablename__ = 'tracking_visit'

    id = db.Column(db.Integer, primary_key=True)
    browser = db.Column(db.String)
    date = db.Column(db.DateTime)
    event = db.Column(db.String)
    url = db.Column(db.String)
    ip_address = db.Column(db.String)
    location = db.Column(db.String)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    site_id = db.Column(db.Integer, db.ForeignKey('tracking_site.id'))
    
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)
    
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
    
    @classmethod
    def query_all(cls):
        return cls.query.all()

    def __repr__(self):
        r = '<Visit for site ID {:d}: {} - {:%Y-%m-%d %H:%M:%S}>'
        return r.format(self.site_id, self.url, self.date)
    

def query_to_list(query, include_field_names=True):
    """Turns a SQLAlchemy query into a list of data values."""
    column_names = []
    for i, obj in enumerate(query.all()):
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)

def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]