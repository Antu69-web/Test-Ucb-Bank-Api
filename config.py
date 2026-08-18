import os
from dotenv import load_dotenv
from datetime import timedelta

# Load variables from .env
load_dotenv()

class Config:
    # This Secret Key is used to create and verify tokens.
    # It is securely loaded from the .env file.
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback_secret')
    
    # Set token expiration to 30 days to avoid frequent log-ins during development
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    SWAGGER = {
        'title': 'UCB Bank API',
        'uiversion': 3,
        'persistAuthorization': True
    }

    # PostgreSQL Database Connection
    # Change '123' to your actual pgAdmin password if it changes
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/ucb_bank_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cloudinary Credentials
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

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
