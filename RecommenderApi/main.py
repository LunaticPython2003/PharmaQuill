from flask import Flask, request, jsonify
from pharmaquill import find_substitute_details
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_substitute', methods=['GET'])
def get_substitute():
    # Extracting medicine_name from query parameters
    medicine_name = request.args.get('medicine_name')

    # Checking if medicine_name is provided
    if not medicine_name:
        return jsonify({'error': 'Missing medicine_name parameter'}), 400

    original_chemical_class, substitutes, substitute_details = find_substitute_details(medicine_name)

    response_data = {
        'original_chemical_class': original_chemical_class,
        'substitutes': substitutes,
        'substitute_details': substitute_details
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
