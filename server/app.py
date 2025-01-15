# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from flask_cors import CORS
from flask_migrate import Migrate

# Local imports
from config import app, db, api  # Import the app, db, and api from config.py
# Add your model imports (PetOwner, PetSitter, etc.)


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

















# original code
# #!/usr/bin/env python3

# # Standard library imports

# # Remote library imports
# from flask import request
# from flask_restful import Resource

# # Local imports
# from config import app, db, api
# # Add your model imports


# # Views go here!

# @app.route('/')
# def index():
#     return '<h1>Project Server</h1>'


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

