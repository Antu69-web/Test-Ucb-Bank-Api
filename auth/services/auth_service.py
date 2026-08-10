from flask_jwt_extended import create_access_token
from auth.models.user import User

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        # Create token
        access_token = create_access_token(
            identity=username,
            additional_claims={"role": user.role}
        )
        return access_token, None
        
    return None, "Invalid credentials"
