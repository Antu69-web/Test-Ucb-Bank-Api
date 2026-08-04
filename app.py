from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flasgger import Swagger

app = Flask(__name__)

# এই সিক্রেট কি (Secret Key) দিয়ে টোকেন তৈরি এবং ভেরিফাই করা হয়। 
# রিয়েল প্রজেক্টে এটি অনেক সিক্রেট রাখতে হয়!
app.config['JWT_SECRET_KEY'] = 'ucb_super_secret_key_123'
jwt = JWTManager(app)

# Swagger Setup
swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "UCB Bank API",
    "description": "API documentation for UCB Bank practice project",
    "version": "1.0.0"
  },
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
    }
  },
  "security": [
    {
      "Bearer": []
    }
  ]
}

app.config['SWAGGER'] = {
    'title': 'UCB Bank API',
    'uiversion': 3
}
swagger = Swagger(app, template=swagger_template)

# --- ডামি ডেটাবেজ (Dummy Database) ---
# আসল প্রজেক্টে এগুলো ডেটাবেজ (যেমন MySQL/PostgreSQL) থেকে আসবে।
# আমরা শেখার জন্য আপাতত একটি লিস্ট ব্যবহার করছি।
users_db = {
    "admin1": {"password": "password123", "role": "admin"},
    "employee1": {"password": "password123", "role": "employee"}
}

customers_data = [
    {"id": 1, "name": "Rahim", "balance": 5000},
    {"id": 2, "name": "Karim", "balance": 10000}
]

# API 1: Login API (সবার জন্য)
# এই এপিআই-তে ইউজারনেম এবং পাসওয়ার্ড দিয়ে রিকোয়েস্ট করলে আমরা একটি টোকেন দেবো।
@app.route('/login', methods=['POST'])
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
    # রিকোয়েস্ট থেকে JSON ডেটা নিচ্ছি
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    # ইউজারনেম ও পাসওয়ার্ড সঠিক কি না চেক করা
    user = users_db.get(username)
    if user and user['password'] == password:
        # টোকেনের ভেতরে আমরা ইউজারের রোল (role) ও সেভ করে রাখছি (additional_claims দিয়ে)
        access_token = create_access_token(
            identity=username, 
            additional_claims={"role": user['role']}
        )
        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    return jsonify({"message": "Invalid username or password"}), 401


# API 2: Get all customers (শুধু Admin এর জন্য)
@app.route('/customers', methods=['GET'])
@jwt_required()  # এর মানে হলো এই এপিআই কল করতে হলে টোকেন লাগবে
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
    # টোকেন থেকে রোল বের করে আনছি
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message": "Access Denied! Only admins can see this."}), 403
    
    return jsonify({"customers": customers_data}), 200


# API 3: Get my profile (Admin এবং Employee উভয়ের জন্য)
@app.route('/my-profile', methods=['GET'])
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
    # কে লগইন করেছে তার নাম বের করা
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        "message": f"Welcome {current_user}",
        "your_role": claims.get("role")
    }), 200


# API 4: Add new customer (শুধু Admin এর জন্য)
@app.route('/add-customer', methods=['POST'])
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


# API 5: Delete a customer (শুধু Admin এর জন্য)
@app.route('/customer/<int:customer_id>', methods=['DELETE'])
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
    
    global customers_data
    # যেই id টি ডিলিট করতে বলা হয়েছে সেটি বাদে বাকিগুলো রেখে দিচ্ছি
    updated_data = [c for c in customers_data if c["id"] != customer_id]
    
    if len(updated_data) == len(customers_data):
        return jsonify({"message": "Customer not found"}), 404
        
    customers_data = updated_data
    return jsonify({"message": f"Customer {customer_id} deleted successfully."}), 200


if __name__ == '__main__':
    app.run(debug=True)
