from flask import Blueprint
from swagger.config import api
from .routes.produto import api as produto_ns

api.add_namespace(produto_ns)

swagger_bp = Blueprint('swagger', __name__, url_prefix='/api')
api.init_app(swagger_bp)