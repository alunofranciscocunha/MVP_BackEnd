from routes.produto import product_route
from database.database import db
from database.models.produto import Produto
from swagger import swagger_bp

# executa todos os métodos de configuração da api
def configure_all(app):
    configure_routes(app)
    configure_db()

# configura as rotas da api
def configure_routes(app):
    # registra um blueprint na aplicação
    app.register_blueprint(product_route, url_prefix='/produtos') # Todas as rotas dentro do blueprint product_routes serão acessíveis com este prefixo /produtos.
    # Registra o blueprint da documentação
    app.register_blueprint(swagger_bp)

# configura o banco de dados
def configure_db():
    db.connect() # conecta ao banco de dados
    db.create_tables([Produto], safe=True) # cria as tabelas no banco de dados, se não existirem