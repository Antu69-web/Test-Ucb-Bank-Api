from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config, swagger_template

# Initialize extensions
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    jwt.init_app(app)
    Swagger(app, template=swagger_template)

    # Register Blueprints from feature modules
    from auth.routes.auth_routes import auth_bp
    from customers.routes.customers_routes import customers_bp
    from workflow.routes.workflow_routes import workflow_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(workflow_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
