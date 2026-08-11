from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from customers.services.customers_service import get_all_customers, add_customer, delete_customer, add_multiple_customers, upload_customers_from_file

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """
    Get all customers (Admin and Employee only)
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of all customers
      401:
        description: Unauthorized (Token missing or invalid)
      403:
        description: "Access forbidden: Admins and Employees only"
    """
    claims = get_jwt()
    if claims.get('role') not in ['admin', 'employee']:
        return jsonify({"message": "Access forbidden: Admins and Employees only"}), 403
        
    return jsonify(get_all_customers()), 200

@customers_bp.route('/customers', methods=['POST'])
@jwt_required()
def post_customer():
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
        description: "Access forbidden: Admins only"
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access forbidden: Admins only"}), 403
    
    data = request.get_json()
    response, status_code = add_customer(data)
    return jsonify(response), status_code

@customers_bp.route('/customers/bulk', methods=['POST'])
@jwt_required()
def post_customers_bulk():
    """
    Bulk add multiple customers at once (Admin only)
    ---
    tags:
      - Customers
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                example: "Hasan"
              balance:
                type: integer
                example: 15000
    responses:
      201:
        description: Customers added successfully
      400:
        description: Invalid format or no valid customers found
      401:
        description: Unauthorized
      403:
        description: "Access forbidden: Admins only"
    """
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403
        
    data = request.get_json()
    response, status_code = add_multiple_customers(data)
    return jsonify(response), status_code

@customers_bp.route('/customers/upload', methods=['POST'])
@jwt_required()
def post_customers_upload():
    """
    Upload an Excel or CSV file to bulk insert customers (Admin only)
    ---
    tags:
      - Customers
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The Excel or CSV file containing customers data (must have 'name' and 'balance' columns)
    responses:
      201:
        description: Customers added successfully
      400:
        description: Invalid file format or missing columns
      401:
        description: Unauthorized
      403:
        description: "Access forbidden: Admins only"
      500:
        description: Failed to process file
    """
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403
        
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    response, status_code = upload_customers_from_file(file)
    return jsonify(response), status_code

@customers_bp.route('/customer/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer_route(customer_id):
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
        description: "Access forbidden: Admins only"
      404:
        description: Customer not found
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access forbidden: Admins only"}), 403
    
    response, status_code = delete_customer(customer_id)
    return jsonify(response), status_code
