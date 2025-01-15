
# Remote library imports
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# Local imports
from config import db  # This imports the db instance defined in config.py

# Models go here!

class PetOwner(db.Model, SerializerMixin):
    __tablename__ = 'pet_owners'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    _hash_password = db.Column(db.String, nullable=False)









# original code
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.ext.associationproxy import association_proxy

# from config import db

# # Models go here!
