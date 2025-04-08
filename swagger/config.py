from flask_restx import Api
from .routes.produto import api as produto_ns

api = Api(
    title='Gerenciador de Produtos', 
    description='API para gerenciamento de produtos, fornecendo endpoints para criar, atualizar, listar e deletar produtos. Tecnologias usadas: Flask, Peewee, Marshmallow, Flask-RESTx.', 
    doc="/docs"
)

api.add_namespace(produto_ns)
