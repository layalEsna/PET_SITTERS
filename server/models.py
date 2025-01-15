
# Remote library imports
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Local imports
from config import db  # This imports the db instance defined in config.py


bcrypt = Bcrypt()
# Models go here!

class PetOwner(db.Model, SerializerMixin):
    __tablename__ = 'pet_owners'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    _hash_password = db.Column(db.String, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,}$')
        if not password or not isinstance(password, str):
            raise ValueError('Password is required and must be string.')
        if not pattern.match(password):
            raise ValueError('Password must be at least 8 characters long. It must include at least 1 lowercase, 1 uppercase letter, and at least 1 (!@#$%^&*)')
        self._hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._hash_password, password)
    
    @validates('user_name')
    def user_name_validate(self, key, user_name):
        if not user_name or not isinstance(user_name, str):
            raise ValueError('Username is required and must be a string.')
        if len(user_name) < 5:
            raise ValueError('Username must be at least 5 characters long.')
        return user_name
    
    serialize_only = ('id', 'user_name')


class PetSitter(db.Model, SerializerMixin):
    __tablename__ = 'pet_sitters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)           
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @validates('name')
    def name_validate(self, key, name):
        if not name or not isinstance(name, str):
            raise ValueError('Name is required and must be a string.')
        return name
    

    def location_validate(self, location):
        geolocator = Nominatim(user_agent="myGeocoder")
        try:
            geo_location = geolocator.geocode(location, timeout=10)  # Increased timeout to 10 seconds
            if geo_location:
                self.latitude = geo_location.latitude
                self.longitude = geo_location.longitude
            else:
                raise ValueError("Unable to geocode the location.")
        except GeocoderTimedOut:
            raise ValueError("Geocoding service timed out.")
        except Exception as e:
            raise ValueError(f"An error occurred during geocoding: {e}")
        
    @validates('price')
    def price_validate(self, key, price):
        if not price or not isinstance(price, int):
            raise ValueError('price is required and must be an integer.')
        if price < 50 or price > 80:
            raise ValueError('Price must be between 50 and 80 inclusive.')
        return price
    
    serialize_only = ('id', 'name', 'location', 'price')


class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

        
















# original code
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.ext.associationproxy import association_proxy

# from config import db

# # Models go here!
