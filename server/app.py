# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session
from flask_restful import Resource
import logging

# Local imports
from config import app, db, api  # Import the app, db, and api from config.py
# Add your model imports (PetOwner, PetSitter, etc.)
from models import PetOwner, PetSitter, Appointment, Pet

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'
class GetSitters(Resource):

    def get(self):

        sitters = [sitter.to_dict()for sitter in PetSitter.query.all()]
        if not sitters:
            return make_response(jsonify({'error': 'No sitters found.'}), 404)
        return make_response(jsonify(sitters), 200)
    
class Signup(Resource):
    def post(self):
            
      try:
        user_name = request.form.get('user_name')
        password =request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([user_name, password, confirm_password]):
            return make_response(jsonify({'error': 'All fields are required'}), 400)
        if password != confirm_password:
            return make_response(jsonify({'error': 'Password not match.'}), 400)
        if PetOwner.query.filter(PetOwner.user_name==user_name).first():
            return make_response(jsonify({'error': 'Username already exists.'}), 400)

        
        new_user = PetOwner(
            user_name = user_name,
            password = password
        )
        
        db.session.add(new_user)
        db.session.commit()
        # session['user_id'] = new_user.id

        response = make_response(jsonify({'message': 'Successful signup'}), 201)
        
        return response
      except Exception as e:
          logging.error(f'Error during signup: {e}')
          return make_response(jsonify({'error': 'Server error.'}), 500)




    
api.add_resource(GetSitters, '/sitters')
api.add_resource(Signup, '/signup')

if __name__ == '__main__':
    app.run(port=5000, debug=True)









# Local:            http://localhost:3000
#   On Your Network:  http://192.168.1.68:3000









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

