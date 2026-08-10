import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Config:
    # This Secret Key is used to create and verify tokens.
    # It is securely loaded from the .env file.
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback_secret')
    
    SWAGGER = {
        'title': 'UCB Bank API',
        'uiversion': 3
    }

    # PostgreSQL Database Connection
    # Change '123' to your actual pgAdmin password if it changes
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/ucb_bank_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
