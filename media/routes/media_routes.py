from flask import Blueprint
from media.controllers.media_controller import upload_media

media_bp = Blueprint('media_bp', __name__)

media_bp.route('/upload', methods=['POST'])(upload_media)
