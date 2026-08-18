from flask import request, jsonify
from media.services.media_service import upload_file_to_cloudinary
from flask_jwt_extended import jwt_required

@jwt_required()
def upload_media():
    """
    Upload media to Cloudinary
    ---
    tags:
      - Media
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: The file to upload (image, video, pdf, doc, etc.)
    responses:
      200:
        description: File uploaded successfully
      400:
        description: No file provided or upload failed
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    uploaded_file = request.files['file']
    
    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        # Call the service to handle the actual upload
        result = upload_file_to_cloudinary(uploaded_file)
        
        # Return the URL received from Cloudinary
        return jsonify({
            "message": "File uploaded successfully",
            "url": result.get('secure_url'),
            "public_id": result.get('public_id')
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
