from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')


from .users import user_bp
api_bp.register_blueprint(user_bp)

from .storage import storage_bp
api_bp.register_blueprint(storage_bp)

from .products import product_bp
api_bp.register_blueprint(product_bp)

from .orders import orders_bp
api_bp.register_blueprint(orders_bp)