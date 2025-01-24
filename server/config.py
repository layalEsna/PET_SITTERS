
# Standard library imports

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# Local imports

# Instantiate app, set attributes
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the React frontend
# CORS(app, resources={r"/*": {"origins": "*"}})


login_manager = LoginManager(app)
login_manager.init_app(app)


app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') 
app.config['SESSION_TYPE'] = 'filesystem'
# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)














# # Standard library imports

# # Remote library imports
# from flask import Flask
# from flask_cors import CORS
# from flask_migrate import Migrate
# from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData

# # Local imports

# # Instantiate app, set attributes
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# # Define metadata, instantiate db
# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })
# db = SQLAlchemy(metadata=metadata)
# migrate = Migrate(app, db)
# db.init_app(app)

# # Instantiate REST API
# api = Api(app)

# # Instantiate CORS
# CORS(app)
