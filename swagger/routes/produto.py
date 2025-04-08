from flask_restx import Namespace, Resource, fields
from database.models.produto import Produto
from database.schemas.produto import ProdutoSchema
from flask import request, jsonify
import datetime

api = Namespace('produtos', description='Operações relacionadas a produtos')

produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)

produto_model = api.model('Produto', {
    'id': fields.Integer(readOnly=True, description='O identificador único do produto', example=1),
    'nome': fields.String(required=True, description='Nome do produto', example='Smartphone Samsung Galaxy S21'),
    'preco': fields.Float(required=True, description='Preço do produto', example=3500.00),
    'quantidade_estoque': fields.Integer(required=True, description='Quantidade em estoque', example=50),
    'codigo_barras': fields.String(description='Código de barras do produto', example='9876543210987'),
    'unidade_medida': fields.String(description='Unidade de medida do produto', example='unidade'),
    'data_cadastro': fields.DateTime(description='Data de cadastro do produto', example='2025-03-23T22:18:47.899Z', dump_only=True),
    'data_atualizacao': fields.DateTime(description='Data de atualização do produto', example='2025-03-23T22:18:47.899Z', dump_only=True)
})

produto_create_model = api.model('ProdutoCreate', {
        'nome': fields.String(required=True, description='Nome do produto', example='Smartphone Samsung Galaxy S21'),
        'preco': fields.Float(required=True, description='Preço do produto', example=3500.00),
        'quantidade_estoque': fields.Integer(required=True, description='Quantidade em estoque', example=50),
        'codigo_barras': fields.String(description='Código de barras do produto', example='9876543210987'),
        'unidade_medida': fields.String(description='Unidade de medida do produto', example='unidade'),
})

produto_update_model = api.model('ProdutoUpdate', {
    'nome': fields.String(description='Nome do produto', example='Smartphone Samsung Galaxy S22'),
    'preco': fields.Float(description='Preço do produto', example=4500.00),
    'quantidade_estoque': fields.Integer(description='Quantidade em estoque', example=30),
    'codigo_barras': fields.String(description='Código de barras do produto', example='1234567890123'),
    'unidade_medida': fields.String(description='Unidade de medida do produto', example='unidade'),
})

@api.route('/')
class ProdutoList(Resource):
    @api.doc('lista_produtos', description='Lista todos os produtos cadastrados')
    @api.marshal_list_with(produto_model)
    def get(self):
        """Lista todos os produtos"""
        produtos = Produto.select()
        return produtos_schema.dump(produtos)

    @api.doc('cadastra_produto', description='Cadastra um novo produto')
    @api.expect(produto_create_model, validate=True)
    @api.marshal_with(produto_model, code=201)
    def post(self):
        """Cadastra um novo produto"""
        data = request.json
        errors = produto_schema.validate(data)
        if errors:
            return errors, 400
        produto = Produto.create(**data)
        return produto_schema.dump(produto), 201

@api.route('/<int:produto_id>')
@api.response(404, 'Produto não encontrado')
@api.param('produto_id', 'O identificador do produto')
class ProdutoResource(Resource):
    @api.doc('busca_produto', description='Busca um produto pelo ID')
    @api.marshal_with(produto_model)
    def get(self, produto_id):
        """Busca um produto pelo ID"""
        try:
            produto = Produto.get_by_id(produto_id)
        except Produto.DoesNotExist:
            api.abort(404, 'Produto não encontrado')
        return produto_schema.dump(produto)

    @api.doc('atualiza_produto', description='Atualiza um produto pelo ID')
    @api.expect(produto_update_model, validate=True)
    @api.marshal_with(produto_model)
    def put(self, produto_id):
        """Atualiza um produto pelo ID"""
        data = request.json
        errors = produto_schema.validate(data, partial=True)
        if errors:
            return errors, 400
        try:
            produto = Produto.get_by_id(produto_id)
        except Produto.DoesNotExist:
            api.abort(404, 'Produto não encontrado')
        for chave, valor in data.items():
            setattr(produto, chave, valor)
        produto.data_atualizacao = datetime.datetime.now()
        produto.save()
        return produto_schema.dump(produto)

    @api.doc('deleta_produto', description='Deleta um produto pelo ID')
    @api.response(204, 'Produto deletado')
    def delete(self, produto_id):
        """Deleta um produto pelo ID"""
        try:
            produto = Produto.get_by_id(produto_id)
        except Produto.DoesNotExist:
            api.abort(404, 'Produto não encontrado')
        produto.delete_instance()
        return '', 204



@api.route('/nome/<string:nome>')
@api.response(404, 'Nenhum produto encontrado com este nome.')
class ProdutoNome(Resource):
    @api.doc('busca_produtos_por_nome', description='Busca produtos pelo nome')
    @api.marshal_list_with(produto_model)
    def get(self, nome):
        """Busca produtos pelo nome"""
        produtos = Produto.select().where(Produto.nome.contains(nome))
        if not produtos:
            api.abort(404, 'Nenhum produto encontrado com este nome.')
        return produtos_schema.dump(produtos)


@api.route('/preco')
@api.response(404, 'Nenhum produto encontrado nesta faixa de preço.')
class ProdutoPreco(Resource):
    @api.doc('busca_produtos_por_preco', description='Busca produtos por faixa de preço passando min_preco e max_preco como query params', params={
        'min_preco': {'description': 'Preço mínimo', 'example': 1000},
        'max_preco': {'description': 'Preço máximo', 'example': 3000}
    })
    @api.marshal_list_with(produto_model)
    def get(self):
        """Busca produtos por faixa de preço"""
        min_preco = request.args.get('min_preco', type=float)
        max_preco = request.args.get('max_preco', type=float)
        
        query = Produto.select()
        if min_preco is not None:
            query = query.where(Produto.preco >= min_preco)
        if max_preco is not None:
            query = query.where(Produto.preco <= max_preco)
        
        produtos = query
        if not produtos:
            api.abort(404, 'Nenhum produto encontrado nesta faixa de preço.')
        return produtos_schema.dump(produtos)