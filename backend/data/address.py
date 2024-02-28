from backend.config import *
from backend.db import *

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String(10), nullable=False)
    street_name = db.Column(db.String(75), nullable=False)
    suburb = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(5), nullable=False)

    
    @classmethod
    def add(cls, db, street_number, street_name, suburb, postcode):
        address = cls(street_number=street_number, street_name=street_name, suburb=suburb, postcode=postcode)
        db.session.add(address)
        return address

    @classmethod
    def get_by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, db, address, street_number, street_name, suburb, postcode):
        address.street_number = street_number
        address.street_name = street_name
        address.suburb = suburb
        address.postcode = postcode
        db.session.commit()
        
    @classmethod
    def delete_by_id(cls, db, id):
        try:
            address = cls.get_by_id(id)
            db.session.delete(address)
            db.session.commit()
            return True
        except Exception as e:
            return False