# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify
from flask_restful import Resource
import logging
from datetime import datetime

# Local imports
from config import app, db, api  # Import the app, db, and api from config.py
# Add your model imports (PetOwner, PetSitter, etc.)
from models import PetOwner, PetSitter, Appointment, Pet

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'




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
        
class Appointment(Resource):
    def post(self):
        
            try:
                data = request.get_json()
                pet_name = data.get('pet_name')
                pet_type = data.get('pet_type')
                date = data.get('date')
                duration = data.get('duration')

                if not all([pet_name, pet_type, date, duration]):
                    return make_response(jsonify({'error': 'All fields are required.'}), 400)
                input_date = datetime.strptime(date, "%Y-%m-%d").date()
                if input_date < datetime.today().date():
                    return make_response(jsonify({'error': 'Date must be in the future.'}), 400)  

                new_appointment = Appointment(
                    pet_name=pet_name,
                    pet_type=pet_type,
                    date=input_date,
                    duration=duration

                ) 
                db.session.add(new_appointment) 
                db.session.commit()       


                return make_response(jsonify(new_appointment.to_dict()), 201)
            except Exception as e:
                  return make_response(jsonify({'error': f'Network or server error: {e}'}),500)

    def patch(self, appointment_id):
        try:
            updated_appointment = Appointment.query.get(appointment_id)
            if not updated_appointment:
                return make_response(jsonify({'error': f'Appointment with ID: {appointment_id} not found.'}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(updated_appointment,key, value)
            db.session.commit()
            return make_response(jsonify(updated_appointment.to_dict()), 200)

        except Exception as e:
            return make_response(jsonify({'error': f'Network or server error: {e}'}), 500)
        
    def delete(self, appointment_id):
      try:
        selected_appointment = Appointment.query.get(appointment_id)

        if not selected_appointment:
            return make_response(jsonify({'error': f'Appointment with ID: {appointment_id} not found'}, 404))
        db.session.delete(selected_appointment)
        db.session.commit()
        return make_response(jsonify({'message': 'Appointment deleted successfully'}), 200)
      except Exception as e:
          return make_response(jsonify({'error': f'Network or server error: {e}'}), 500)


             
api.add_resource(GetSitters, '/sitters', '/sitters/<int:sitter_id>')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Appointment, '/appointment', '/appointment/<int:appointment_id>')

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

