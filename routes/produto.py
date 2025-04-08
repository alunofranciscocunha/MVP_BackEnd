from flask import Blueprint, request, jsonify
from database.models.produto import Produto
from database.schemas.produto import ProdutoSchema
from peewee import IntegrityError
import datetime

product_route = Blueprint('produto', __name__)
produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)

@product_route.route('/')
def lista_produtos():
    """ Lista todos os produtos cadastrados """
    produtos = Produto.select()
    # converte o objeto em um formato que pode ser facilmente armazenado ou transmitido
    result = produtos_schema.dump(produtos)
    return jsonify(result)

@product_route.route('/', methods=['POST'])
def cadastra_produto():
    """ Cadastra um novo produto """
    data = request.json

    # verifica se os dados fornecidos estão em conformidade com as regras de validacoes definidas no esquema
    errors = produto_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    try:
        produto = Produto.create(**data)
    except IntegrityError as e:
        if 'UNIQUE constraint failed: produto.codigo_barras' in str(e):
            return jsonify({'error': 'Código de barras já foi cadastrado em outro produto'}), 400
        else:
            return jsonify({'error': 'Erro ao cadastrar o produto'}), 400

    result = produto_schema.dump(produto)
    return jsonify(result), 201

@product_route.route('/<int:produto_id>', methods=['GET'])
def busca_produto(produto_id):
    """ Busca um produto pelo ID """
    try:
        produto = Produto.get_by_id(produto_id)
    except Produto.DoesNotExist:
        return jsonify({'error': 'Produto não encontrado.'}), 404

    result = produto_schema.dump(produto)
    return jsonify(result)

@product_route.route('/<int:produto_id>', methods=['PUT'])
def atualiza_produto(produto_id):
    """ Atualiza um produto pelo ID """
    data = request.json
    # verifica se os dados parciais recebidos estão em conformidade com as regras de validacoes definidas no esquema
    errors = produto_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    try:
        produto = Produto.get_by_id(produto_id)
    except Produto.DoesNotExist:
        return jsonify({'error': 'Produto não encontrado.'}), 404

    for chave, valor in data.items():
        setattr(produto, chave, valor)

    produto.data_atualizacao = datetime.datetime.now()
    produto.save()
    
    result = produto_schema.dump(produto)
    return jsonify(result)

@product_route.route('/<int:produto_id>', methods=['DELETE'])
def deleta_produto(produto_id):
    """ Deleta um produto pelo ID """
    try:
        produto = Produto.get_by_id(produto_id)
    except Produto.DoesNotExist:
        return jsonify({'error': 'Produto não encontrado.'}), 404

    produto.delete_instance()
    return jsonify({'message': 'Produto deletado com sucesso.'}), 200


@product_route.route('/nome/<string:nome>', methods=['GET'])
def busca_produtos_por_nome(nome):
    """ Busca produtos pelo nome """
    produtos = Produto.select().where(Produto.nome.contains(nome))
    if not produtos:
        return jsonify({'error': 'Nenhum produto encontrado com este nome.'}), 404

    resultado = produtos_schema.dump(produtos)
    return jsonify(resultado)


@product_route.route('/preco', methods=['GET'])
def busca_produtos_por_preco():
    """ Busca produtos por faixa de preço """
    min_preco = request.args.get('min_preco', type=float)
    max_preco = request.args.get('max_preco', type=float)
    
    query = Produto.select()
    if min_preco is not None:
        query = query.where(Produto.preco >= min_preco)
    if max_preco is not None:
        query = query.where(Produto.preco <= max_preco)
    
    produtos = query
    if not produtos:
        return jsonify({'error': 'Nenhum produto encontrado nesta faixa de preço.'}), 404

    resultado = produtos_schema.dump(produtos)
    return jsonify(resultado)