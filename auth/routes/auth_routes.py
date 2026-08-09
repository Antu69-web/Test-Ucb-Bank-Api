from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from database.dummy_db import users_db

auth_bp = Blueprint('auth', __name__)

# API 1: Login API (For Everyone)
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login to get JWT token
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin1
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid username or password
    """
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    user = users_db.get(username)
    if user and user['password'] == password:
        access_token = create_access_token(
            identity=username, 
            additional_claims={"role": user['role']}
        )
        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    return jsonify({"message": "Invalid username or password"}), 401


# API 3: Get my profile (For both Admin and Employee)
@auth_bp.route('/my-profile', methods=['GET'])
@jwt_required()
def my_profile():
    """
    Get my profile
    ---
    tags:
      - Profile
    responses:
      200:
        description: User profile details
      401:
        description: Unauthorized
    """
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        "message": f"Welcome {current_user}",
        "your_role": claims.get("role")
    }), 200
