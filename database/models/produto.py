from peewee import Model, CharField, IntegerField, DecimalField, DateTimeField
from database.database import db
import datetime

class Produto(Model):
    nome = CharField()
    preco = DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = IntegerField()
    codigo_barras = CharField(null=True, unique=True)
    unidade_medida = CharField()
    data_cadastro = DateTimeField(default=datetime.datetime.now)
    data_atualizacao = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db