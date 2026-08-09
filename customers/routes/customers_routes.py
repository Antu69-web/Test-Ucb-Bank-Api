from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from database.dummy_db import customers_data

customers_bp = Blueprint('customers', __name__)

# API 2: Get all customers (Admin only)
@customers_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """
    Get all customers (Admin only)
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of all customers
      401:
        description: Unauthorized (Token missing or invalid)
      403:
        description: Access Denied! Only admins can see this.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can see this."}), 403
    
    return jsonify({"customers": customers_data}), 200


# API 4: Add new customer (Admin only)
@customers_bp.route('/add-customer', methods=['POST'])
@jwt_required()
def add_customer():
    """
    Add a new customer (Admin only)
    ---
    tags:
      - Customers
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Hasan
            balance:
              type: integer
              example: 15000
    responses:
      201:
        description: Customer added successfully
      401:
        description: Unauthorized
      403:
        description: Access Denied! Only admins can add customers.
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can add customers."}), 403
    
    data = request.get_json()
    new_customer = {
        "id": len(customers_data) + 1,
        "name": data.get("name"),
        "balance": data.get("balance", 0)
    }
    customers_data.append(new_customer)
    return jsonify({"message": "Customer added successfully", "customer": new_customer}), 201


# API 5: Delete a customer (Admin only)
@customers_bp.route('/customer/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    """
    Delete a customer (Admin only)
    ---
    tags:
      - Customers
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
        description: The ID of the customer to delete
    responses:
      200:
        description: Customer deleted successfully
      401:
        description: Unauthorized
      403:
        description: Access Denied! Only admins can delete customers.
      404:
        description: Customer not found
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can delete customers."}), 403
    
    updated_data = [c for c in customers_data if c["id"] != customer_id]
    
    if len(updated_data) == len(customers_data):
        return jsonify({"message": "Customer not found"}), 404
        
    customers_data.clear()
    customers_data.extend(updated_data)
    return jsonify({"message": f"Customer {customer_id} deleted successfully."}), 200
