from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import creds
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


client = MongoClient(creds.APP_URI, server_api=ServerApi('1'))
db = client.pharmaQuill
doctors_collection = db.doctors

class DoctorResource(Resource):
    def post(self):
        try:

            data = request.get_json()

            doctor_name = data.get('doctor_name')
            doctor_code = data.get('doctor_code')
            specialization = data.get('specialization')
            pharmacy_name = data.get('pharmacy_name')
            timing = data.get('timing')
            charges = data.get('charges')
            email = data.get('email')
            phone_number = data.get('phone_number')
            street_address = data.get('street_address')
            city = data.get('city')
            state = data.get('state')
            zip_code = data.get('zip_code')
            medical_degree = data.get('medical_degree')
            medical_school = data.get('medical_school')
            graduation_year = data.get('graduation_year')
            board_certification = data.get('board_certification')
            years_of_experience = data.get('years_of_experience')
            previous_institutions = data.get('previous_institutions')
            license_number = data.get('license_number')
            license_expiry_date = data.get('license_expiry_date')
            accepted_insurance_plans = data.get('accepted_insurance_plans')
            languages_spoken = data.get('languages_spoken')
            days_available = data.get('days_available')
            working_hours = data.get('working_hours')
            appointment_fee = data.get('appointment_fee')
            booking_system = data.get('booking_system')
            additional_notes = data.get('additional_notes')

            # Insert data into the doctors collection
            doctor_data = {
                'doctor_name': doctor_name,
                'doctor_code': doctor_code,
                'specialization': specialization,
                'pharmacy_name': pharmacy_name,
                'timing': timing,
                'charges': charges,
                'email': email,
                'phone_number': phone_number,
                'street_address': street_address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'medical_degree': medical_degree,
                'medical_school': medical_school,
                'graduation_year': graduation_year,
                'board_certification': board_certification,
                'years_of_experience': years_of_experience,
                'previous_institutions': previous_institutions,
                'license_number': license_number,
                'license_expiry_date': license_expiry_date,
                'accepted_insurance_plans': accepted_insurance_plans,
                'languages_spoken': languages_spoken,
                'days_available': days_available,
                'working_hours': working_hours,
                'appointment_fee': appointment_fee,
                'booking_system': booking_system,
                'additional_notes': additional_notes
            }
            result = doctors_collection.insert_one(doctor_data)

            return {'status': 'success', 'message': 'Doctor added successfully!', 'inserted_id': str(result.inserted_id)}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

class AllDoctorsResource(Resource):
    def get(self):
        try:
            # Retrieve all doctors from MongoDB
            all_doctors = list(doctors_collection.find())

            formatted_doctors = []
            for doctor in all_doctors:
                doctor['_id'] = str(doctor['_id'])
                formatted_doctors.append(doctor)

            return {'status': 'success', 'doctors': formatted_doctors}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Add the DoctorResource and AllDoctorsResource to the API
api.add_resource(DoctorResource, '/doctors')
api.add_resource(AllDoctorsResource, '/all_doctors')

if __name__ == '__main__':
    app.run(debug=True)
