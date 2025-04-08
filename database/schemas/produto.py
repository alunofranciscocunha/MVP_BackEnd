from marshmallow import Schema, fields

# Esquema de validação e serialização para objetos do tipo Produto
class ProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    preco = fields.Decimal(required=True, as_string=True)
    quantidade_estoque = fields.Int(required=True)
    codigo_barras = fields.Str()
    unidade_medida = fields.Str()
    data_cadastro = fields.DateTime(dump_only=True)
    data_atualizacao = fields.DateTime(dump_only=True)