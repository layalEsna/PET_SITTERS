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
    
    def get_sitter_by_id(self, id):
        try:
            sitter = PetSitter.query.filter(PetSitter.id==id).first()
            if not sitter:
                return make_response(jsonify({'error': f'Sitter with ID: {id} not found'}), 404)
            return make_response(jsonify(sitter), 200)
        except Exception as e:
            logging.error('Failed to get sitter.')
            return make_response(jsonify({'error': f'Network or server error: {e}'}), 500)

class Signup(Resource):
    def options(self):
        return '', 200

    def post(self):
        try:
            user_name = request.form.get('user_name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if not all([user_name, password, confirm_password]):
                return make_response(jsonify({'error': 'All fields are required'}), 400)

            if password != confirm_password:
                return make_response(jsonify({'error': 'Password not match.'}), 400)

            if PetOwner.query.filter(PetOwner.user_name == user_name).first():
                return make_response(jsonify({'error': 'Username already exists.'}), 400)

            
            new_user = PetOwner(
                user_name=user_name,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            response = make_response(jsonify({'message': 'Successful signup'}), 201)
            return response

        except Exception as e:
            logging.error(f'Error during signup: {e}')
            return make_response(jsonify({'error': 'Server error.'}), 500)
    
class Login(Resource):

    def user_login(self):
        print("Login request received!")

        try:
            user_name = request.form.get('user_name')
            password = request.form.get('password')

            if not all([user_name, password]):
                return make_response(jsonify({'error': 'All fields are required.'}), 400)
            user = PetOwner.query.filter(PetOwner.user_name==user_name).first()
            if not user:
                return make_response(jsonify({'error': 'Invalid username or password.'}), 401)
            if not user.check_password(password):
                return make_response(jsonify({'error': 'Invalid username or password.'}), 401)
            return make_response(jsonify({'message': 'Successful login.'}), 200)
        except Exception as e:
            logging.error(f'An error occured during login: {e}')
            return make_response(jsonify({'error': 'Network or server error.'}), 500)



# class Login(Resource):
#     def post(self):
#         try:
#             user_name = request.form.get('user_name')
#             password = request.form.get('password')

#             if not all([user_name, password]):
#                 return make_response(jsonify({'error': 'All fields are required.'}), 400)

#             user = PetOwner.query.filter(PetOwner.user_name == user_name).first()
#             if not user:
#                 return make_response(jsonify({'error': 'Invalid username or password.'}), 401)

#             if not user.check_password(password):
#                 return make_response(jsonify({'error': 'Invalid username or password.'}), 401)

#             return make_response(jsonify({'message': 'Successful login.'}), 200)

#         except Exception as e:
#             logging.error(f'An error occurred during login: {e}')
#             return make_response(jsonify({'error': 'Network or server error.'}), 500)
             
api.add_resource(GetSitters, '/sitters')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')

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

