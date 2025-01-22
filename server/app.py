# Standard library imports

# Remote library imports
from dotenv import load_dotenv
load_dotenv()
import os
from flask import request, make_response, jsonify, session
from flask_restful import Resource
import logging
from datetime import datetime
print("FLASK_SECRET_KEY:", os.environ.get('FLASK_SECRET_KEY'))  # Add this line

# Local imports
from config import app, db, api  # Import the app, db, and api from config.py
# Add your model imports (PetOwner, PetSitter, etc.)
from models import PetOwner, PetSitter, Appointment, Pet

# Views go here!
class ShowSession(Resource):
    
    def get(self, key):
        session['hello'] = session.get('hello') or 'World'
        session['goodnight'] = session.get('goodnight') or 'Moon'

        response = make_response(jsonify({
            'session': {
                'session_key': key,
                'session_value': session.get(key, 'Key not found'),
                'session_accessed': session.modified,
            },
            'cookies': [{cookie: request.cookies[cookie]} for cookie in request.cookies],
        }), 200)

        response.set_cookie('mouse', 'Cookie')
        return response




class GetSitters(Resource):

    def get(self, sitter_id=None):  
        try:
            if sitter_id: 
                sitter = PetSitter.query.get(sitter_id)
                if not sitter:
                    return make_response(jsonify({'error': f'Sitter with ID: {sitter_id} not found'}), 404)
                return make_response(jsonify(sitter.to_dict()), 200)

            
            sitters = [sitter.to_dict() for sitter in PetSitter.query.all()]
            if not sitters:
                return make_response(jsonify({'error': 'No sitters found.'}), 404)
            return make_response(jsonify(sitters), 200)

        except Exception as e:
            logging.error(f'Error fetching sitter(s): {e}')
            return make_response(jsonify({'error': 'Internal server error'}), 500)

class Signup(Resource):
    def options(self):
        return '', 200

    def post(self):
        try:
            data = request.get_json()
            user_name = data.get('user_name')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

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

            session['user_id'] = new_user.id

            response = make_response(jsonify({'message': 'Successful signup'}), 201)
            return response

        except Exception as e:
            logging.error(f'Error during signup: {e}')
            return make_response(jsonify({'error': 'Server error.'}), 500)


class Login(Resource):
    def post(self): 
        print("Login request received!")

        try:
            data = request.get_json()
            user_name = data.get('user_name')
            password = data.get('password')

            if not all([user_name, password]):
                return make_response(jsonify({'error': 'All fields are required.'}), 400)

            user = PetOwner.query.filter(PetOwner.user_name == user_name).first()
            if not user:
                return make_response(jsonify({'error': 'Invalid username or password.'}), 401)

            if not user.check_password(password):
                return make_response(jsonify({'error': 'Invalid username or password.'}), 401)

            session['user_id'] = user.id 
            print(f"Session user_id after login: {session.get('user_id')}")
            return make_response(jsonify({'message': 'Successful login.'}), 200)

        except Exception as e:
            logging.error(f'An error occurred during login: {e}')
            return make_response(jsonify({'error': 'Network or server error.'}), 500)
        
class Appointment(Resource):
    def post(self):
            print("POST /appointment endpoint called")
        
            try:
                data = request.get_json()
                print("Received data:", data)
                pet_name = data.get('pet_name')
                pet_type = data.get('pet_type')
                date = data.get('date')
                duration = data.get('duration')
                sitters_id = data.get('sitters_id')
                pet_owners_id = data.get('pet_owners_id') or session.get('user_id')
                print(f"Session user_id: {pet_owners_id}")  # Add this to your POST method in Appointment

                if not all([pet_name, pet_type, date, duration, sitters_id, pet_owners_id]):
                    return make_response(jsonify({'error': 'All fields are required.'}), 400)
                try:
                    input_date = datetime.strptime(date, "%Y-%m-%d").date()
                    if input_date < datetime.today().date():
                        return make_response(jsonify({'error': 'Date must be in the future.'}), 400)  
                except ValueError:
                    return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400)
                
                new_appointment = Appointment(
                    
                    date=input_date,
                    duration=duration,
                    pet_owners_id=pet_owners_id,
                    sitters_id=sitters_id

                ) 
                db.session.add(new_appointment) 
                db.session.commit()       


                return make_response(jsonify({'appointment':new_appointment.to_dict()}), 201)
            except Exception as e:
                  return make_response(jsonify({'error': f'Network or server error: {e}'}),500)
            


    def patch(self, id):
        print(f"PATCH /appointment/{id} endpoint called")
        try:
            updated_appointment = Appointment.query.get(id)
            if not updated_appointment:
                return make_response(jsonify({'error': f'Appointment with ID: {id} not found.'}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(updated_appointment,key, value)
            db.session.commit()
            return make_response(jsonify(updated_appointment.to_dict()), 200)

        except Exception as e:
            return make_response(jsonify({'error': f'Network or server error: {e}'}), 500)





    def delete(self, id):
      try:
        selected_appointment = Appointment.query.get(id)

        if not selected_appointment:
            return make_response(jsonify({'error': f'Appointment with ID: {id} not found'}, 404))
        db.session.delete(selected_appointment)
        db.session.commit()
        return make_response(jsonify({'message': 'Appointment deleted successfully'}), 200)
      except Exception as e:
          return make_response(jsonify({'error': f'Network or server error: {e}'}), 500)

api.add_resource(ShowSession, '/sessions/<string:key>')
             
api.add_resource(GetSitters, '/sitters', '/sitters/<int:sitter_id>')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Appointment,'/appointment' ,'/appointment/<int:id>')

if __name__ == '__main__':
    
    app.run(port=5000, debug=True, use_reloader=True)









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

