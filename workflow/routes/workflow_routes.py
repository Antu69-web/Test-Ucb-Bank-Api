from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from workflow.services.workflow_service import request_loan as req_loan_service, get_pending_loans as get_pend_service, approve_loan as approve_service, reject_loan as reject_service

workflow_bp = Blueprint('workflow', __name__)

@workflow_bp.route('/loan/request', methods=['POST'])
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
    response, status_code = req_loan_service(data)
    return jsonify(response), status_code

@workflow_bp.route('/loan/pending', methods=['GET'])
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
        
    return jsonify({"pending_requests": get_pend_service()}), 200

@workflow_bp.route('/loan/approve/<int:request_id>', methods=['POST'])
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
        
    response, status_code = approve_service(request_id)
    return jsonify(response), status_code

@workflow_bp.route('/loan/reject/<int:request_id>', methods=['POST'])
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
        
    response, status_code = reject_service(request_id)
    return jsonify(response), status_code
