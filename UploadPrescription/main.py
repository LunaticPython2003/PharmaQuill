from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import creds
import base64

app = Flask(__name__)
api = Api(app)

# Set the Stable API version when creating a new client
client = MongoClient(creds.APP_URI, server_api=ServerApi('1'))
db = client.pharmaQuill
prescriptions_collection = db.prescriptions

class PrescriptionResource(Resource):
    def post(self):
        try:
            # Get form data from the request
            data = request.form

            # Extract fields from the form data
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            address = data.get('address')
            contact_details = data.get('contact_details')
            date = data.get('date')
            time = data.get('time')

            # Handle image file upload
            image_file = request.files['image']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Insert data into the prescriptions collection
            prescription_data = {
                'name': name,
                'age': age,
                'gender': gender,
                'address': address,
                'contact_details': contact_details,
                'date': date,
                'time': time,
                'image': image_data
            }
            result = prescriptions_collection.insert_one(prescription_data)

            return {'status': 'success', 'message': 'Prescription added successfully!', 'inserted_id': str(result.inserted_id)}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

class AllPrescriptionsResource(Resource):
    def get(self):
        try:
            # Retrieve all prescriptions from MongoDB
            all_prescriptions = list(prescriptions_collection.find())

            # Format the prescriptions data
            formatted_prescriptions = []
            for prescription in all_prescriptions:
                prescription['_id'] = str(prescription['_id'])  # Convert ObjectId to string
                formatted_prescriptions.append(prescription)

            return {'status': 'success', 'prescriptions': formatted_prescriptions}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Add the PrescriptionResource and AllPrescriptionsResource to the API
api.add_resource(PrescriptionResource, '/prescriptions')
api.add_resource(AllPrescriptionsResource, '/all_prescriptions')

if __name__ == '__main__':
    app.run(debug=True)
