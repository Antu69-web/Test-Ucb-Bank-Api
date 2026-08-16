from flask import Flask, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from config import Config, swagger_template
from database.db import db

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    Swagger(app, template=swagger_template)
    JWTManager(app)
    db.init_app(app)
    
    # Register Blueprints
    from auth.routes.auth_routes import auth_bp
    from customers.routes.customers_routes import customers_bp
    from workflow.routes.workflow_routes import workflow_bp
    from calculator.routes.calculator_routes import calculator_bp
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(customers_bp, url_prefix='/')
    app.register_blueprint(workflow_bp, url_prefix='/workflow')
    app.register_blueprint(calculator_bp, url_prefix='/calculator')
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to UCB Bank API. Go to /apidocs/ for documentation."})
        
    # Create tables and initial data
    with app.app_context():
        db.create_all()
        # Seed initial data if tables are empty
        from auth.models.user import User
        from customers.models.customer import Customer
        if User.query.count() == 0:
            db.session.add(User(username='admin1', password='password123', role='admin'))
            db.session.add(User(username='employee1', password='password123', role='employee'))
            db.session.commit()
            
        if Customer.query.count() == 0:
            db.session.add(Customer(name='Rahim', balance=5000))
            db.session.add(Customer(name='Karim', balance=10000))
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
