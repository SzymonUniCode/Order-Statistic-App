from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')


from .users import user_bp
api_bp.register_blueprint(user_bp)