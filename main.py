from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from ListDoctors.main import DoctorResource, AllDoctorsResource
from UploadPrescription.main import PrescriptionResource, AllPrescriptionsResource
from Orders.main import OrderResource, UpdateCanFulfillResource, OrderStatusResource, OrdersByPharmacyResource,RejectOrderResource
# from RecommenderApi.main import app as substitutes_app

app = Flask(__name__)
api = Api(app)
CORS(app)

# Add doctors-related resources
api.add_resource(DoctorResource, '/doctors')
api.add_resource(AllDoctorsResource, '/all_doctors')

# Add prescriptions-related resources
api.add_resource(PrescriptionResource, '/prescriptions')
api.add_resource(AllPrescriptionsResource, '/all_prescriptions')

# Add orders-related resources
api.add_resource(OrderResource, "/orders")
api.add_resource(UpdateCanFulfillResource, "/update_can_fulfill/<order_id>")
api.add_resource(OrderStatusResource, "/order_status/<order_id>")
api.add_resource(OrdersByPharmacyResource, "/orders_by_pharmacy")
# api.add_resource(RejectOrderResource, "/reject_order/<order_id>")

# # Include substitutes-related app
# app.register_blueprint(substitutes_app)

if __name__ == '__main__':
    app.run(debug=True)
