# Gerenciador de Produtos API

## Descrição
A API Gerenciador de Produtos é uma aplicação desenvolvida com Flask, Peewee e Marshmallow, que fornece endpoints para criar, atualizar, listar e deletar produtos. A documentação da API é gerada utilizando Flask-RESTx.

## Tecnologias Utilizadas
- Flask
- Peewee
- Marshmallow
- Flask-RESTx
- Flask_cors

## Dependências
- Python 3.13.2

## Instalação do Python

Se você não tem o Python instalado, siga os passos abaixo:

1. Baixe o instalador do Python em [python.org](https://www.python.org/downloads/).
2. Execute o instalador e siga as instruções na tela.
3. Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.

**Observação:** Certifique-se de baixar e instalar a versão 3.13.2 do Python.

## Instalação
1. Clone o repositório:
    ```sh
    git clone https://github.com/alunofranciscocunha/MVP_BackEnd.git
    ```
2. Navegue até o diretório do projeto:
    ```sh
    cd MVP_BackEnd
    ```
3. Crie um ambiente virtual:
    ```sh
    python -m venv venv
    ```
4. Ative o ambiente virtual:
    - Windows:
        ```sh
        venv\Scripts\activate
        ```
    - Unix/MacOS:
        ```sh
        source venv/bin/activate
        ```
5. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Execução
1. Execute a aplicação:
    ```sh
    python main.py
    ```
2. A API estará disponível em `http://127.0.0.1:5000`.

## Endpoints
### Produtos
- **GET /produtos/**: Lista todos os produtos cadastrados.
- **POST /produtos/**: Cadastra um novo produto.
- **GET /produtos/{produto_id}**: Busca um produto pelo ID.
- **PUT /produtos/{produto_id}**: Atualiza um produto pelo ID.
- **DELETE /produtos/{produto_id}**: Deleta um produto pelo ID.
- **GET /produtos/nome/{nome}**: Busca produtos pelo nome.
- **GET /produtos/preco?min_preco={min_preco}&max_preco={max_preco}**: Busca produtos por faixa de preço.

### Documentação
A documentação da API está disponível em `http://127.0.0.1:5000/api/docs`.

## Estrutura do Projeto
```plaintext
ProductManagerAPI/
├── database/               # Contém a configuração do banco de dados e os modelos
│   ├── models/             # Modelos do banco de dados
│   │   └── produto.py
│   ├── schemas/            # Schemas de validação e serialização
│   │   └── produto.py
│   └── database.py         # Configuração do banco de dados
├── routes/                 # Rotas da API
│   └── produto.py
├── swagger/                # Configuração e rotas da documentação da API
│   ├── routes/
│   │   └── produto.py
│   ├── __init__.py
│   └── config.py
├── .gitignore              # Arquivo para ignorar arquivos e pastas no Git
├── config.py               # Configuração da aplicação
├── main.py                 # Arquivo principal para executar a aplicação
├── README.md               # Documentação do projeto
└── requirements.txt        # Dependências do projeto
```

## Contribuição
1. Faça um fork do projeto.
2. Crie uma branch para sua feature:
    ```sh
    git checkout -b feature/nova-feature
    ```
3. Commit suas mudanças:
    ```sh
    git commit -am 'Adiciona nova feature'
    ```
4. Faça um push para a branch:
    ```sh
    git push origin feature/nova-feature
    ```
5. Abra um Pull Request.
