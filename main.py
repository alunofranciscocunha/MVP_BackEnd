from flask import Flask
from config import configure_all
from flask_cors import CORS

# inicializacao da API
app = Flask(__name__)
CORS(app)  # Permite CORS para todas as rotas

#configuracao da API
configure_all(app)

# execucao da API
app.run(debug=True)