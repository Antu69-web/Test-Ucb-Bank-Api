from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from database.dummy_db import loan_requests_data, customers_data
from workflow.services.workflow_service import process_loan_approval, process_loan_rejection

workflow_bp = Blueprint('workflow', __name__)

@workflow_bp.route('/workflow/loan/request', methods=['POST'])
@jwt_required()
def request_loan():
    """
    Employee requests a loan for a customer
    ---
    tags:
      - Workflow
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: integer
              example: 1
            amount:
              type: integer
              example: 50000
    responses:
      201:
        description: Loan request submitted
      403:
        description: Only employees can request loans
      404:
        description: Customer not found
    """
    claims = get_jwt()
    if claims.get("role") != "employee":
        return jsonify({"message": "Access Denied! Only employees can submit loan requests."}), 403
    
    data = request.get_json()
    customer_id = data.get("customer_id")
    amount = data.get("amount")
    
    # Check if customer exists
    if not any(c['id'] == customer_id for c in customers_data):
        return jsonify({"message": "Customer not found."}), 404
        
    new_request = {
        "id": len(loan_requests_data) + 1,
        "customer_id": customer_id,
        "amount": amount,
        "status": "pending"
    }
    loan_requests_data.append(new_request)
    
    return jsonify({"message": "Loan request submitted to workflow.", "request": new_request}), 201

@workflow_bp.route('/workflow/loan/pending', methods=['GET'])
@jwt_required()
def get_pending_loans():
    """
    Admin views all pending loan requests
    ---
    tags:
      - Workflow
    responses:
      200:
        description: A list of pending loan requests
      403:
        description: Only admins can view pending requests
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can view pending requests."}), 403
        
    pending = [r for r in loan_requests_data if r['status'] == 'pending']
    return jsonify({"pending_requests": pending}), 200

@workflow_bp.route('/workflow/loan/approve/<int:request_id>', methods=['POST'])
@jwt_required()
def approve_loan(request_id):
    """
    Admin approves a loan request
    ---
    tags:
      - Workflow
    parameters:
      - name: request_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Loan approved
      400:
        description: Bad request (already processed or not found)
      403:
        description: Only admins can approve loans
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can approve loans."}), 403
        
    success, message = process_loan_approval(request_id)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400

@workflow_bp.route('/workflow/loan/reject/<int:request_id>', methods=['POST'])
@jwt_required()
def reject_loan(request_id):
    """
    Admin rejects a loan request
    ---
    tags:
      - Workflow
    parameters:
      - name: request_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Loan rejected
      400:
        description: Bad request (already processed or not found)
      403:
        description: Only admins can reject loans
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can reject loans."}), 403
        
    success, message = process_loan_rejection(request_id)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400
