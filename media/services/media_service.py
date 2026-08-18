import cloudinary.uploader

def upload_file_to_cloudinary(file):
    """
    Uploads a file (image, video, pdf, etc.) to Cloudinary and returns the response.
    """
    upload_result = cloudinary.uploader.upload(
        file,
        folder="ucb_bank_media",
        resource_type="auto"
    )
    return upload_result
