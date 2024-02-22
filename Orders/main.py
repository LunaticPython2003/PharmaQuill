from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from flask_cors import CORS
import creds

app = Flask(__name__)
api = Api(app)
CORS(app)

client = MongoClient(creds.APP_URI, server_api=ServerApi("1"))
db = client.pharmaQuill
orders_collection = db.orders
prescriptions_collection = db.prescriptions


class OrderResource(Resource):
    def post(self):
        try:
            data = request.get_json()

            # Check if pharmacy can provide all meds in the prescription
            pharmacy_name = data.get("pharmacy_name")
            prescription_id = data.get("prescription_id")

            # Assuming you have a function to check if the pharmacy can fulfill the order
            can_fulfill = self.can_fulfill_order(pharmacy_name, prescription_id)

            # Insert data into the orders collection
            order_data = {
                "prescription_id": prescription_id,
                "pharmacy_name": pharmacy_name,
                "can_fulfill": can_fulfill,
                "order_status": "pending" if can_fulfill else "rejected",
            }

            result = orders_collection.insert_one(order_data)

            return {
                "status": "success",
                "message": "Order placed successfully!",
                "inserted_id": str(result.inserted_id),
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def can_fulfill_order(self, pharmacy_name, prescription_id):
        order_document = orders_collection.find_one(
            {"pharmacy_name": pharmacy_name, "prescription_id": prescription_id}
        )
        return order_document and order_document.get("can_fulfill") is True


class UpdateCanFulfillResource(Resource):
    def put(self, order_id):
        try:
            data = request.get_json()

            ordered_meds = data.get("ordered_meds", [])

            orders_collection.update_one(
                {"_id": ObjectId(order_id)},
                {
                    "$set": {
                        "can_fulfill": True,
                        "ordered_meds": ordered_meds,
                        "order_status": "pending",
                    }
                },
            )

            return {
                "status": "success",
                "message": "can_fulfill status updated to True and order status set to pending!",
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}


class OrderStatusResource(Resource):
    def put(self, order_id):
        try:
            orders_collection.update_one(
                {"_id": ObjectId(order_id)}, {"$set": {"order_status": "completed"}}
            )

            return {
                "status": "success",
                "message": "Order status updated to completed!",
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}


class OrdersByPharmacyResource(Resource):
    def get(self):
        try:
            # Extract pharmacy_name from the URL parameters
            pharmacy_name = request.args.get("pharmacy_name")

            pharmacy_orders = list(
                orders_collection.find({"pharmacy_name": pharmacy_name})
            )

            orders_with_prescription_details = []
            for order in pharmacy_orders:
                prescription_details = self.get_prescription_details(
                    order["prescription_id"]
                )
                # Convert ObjectId to string for serialization
                order["_id"] = str(order["_id"])
                order["prescription_details"] = prescription_details
                orders_with_prescription_details.append(order)

            return {
                "status": "success",
                "orders": orders_with_prescription_details,
                "pharmacy_name": pharmacy_name,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_prescription_details(self, prescription_id):
        # Retrieve prescription details from the 'prescriptions' collection based on the prescription_id
        prescription = prescriptions_collection.find_one({'_id': ObjectId(prescription_id)})
        # Convert ObjectId to string for serialization
        prescription['_id'] = str(prescription['_id'])
        return prescription


class RejectOrderResource(Resource):
    def put(self, order_id):
        try:
            orders_collection.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": {"can_fulfill": False, "order_status": "rejected"}},
            )

            return {"status": "success", "message": "Order status updated to rejected!"}

        except Exception as e:
            return {"status": "error", "message": str(e)}


api.add_resource(OrderResource, "/orders")
api.add_resource(UpdateCanFulfillResource, "/update_can_fulfill/<order_id>")
api.add_resource(OrderStatusResource, "/order_status/<order_id>")
api.add_resource(OrdersByPharmacyResource, "/orders_by_pharmacy")
api.add_resource(RejectOrderResource, "/reject_order/<order_id>")

if __name__ == "__main__":
    app.run(debug=True)
