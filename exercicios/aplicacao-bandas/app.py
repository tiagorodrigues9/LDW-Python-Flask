from flask import Flask, render_template
from controllers import routes
import pymysql
from models.database import db

app = Flask(__name__, template_folder='views')

routes.init_app(app)

# Define o nome do banco de dados
DB_NAME = 'wikimusic'
# Configura o Flask com o banco definido
app.config['DATABASE_NAME'] = DB_NAME

# Passando o endereço do banco ao Flask
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root@localhost/{DB_NAME}'

# Iniciando o servidor no localhost, porta 5000, modo de depuração ativado
if __name__ == '__main__':
    # Criando os dados de conexão:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # Tentando criar o banco
    # Try, trata o sucesso
    try:
        # with cria um recurso temporariamente
        with connection.cursor() as cursor:  # alias
            # Cria o banco de dados (se ele não existir)
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"O banco de dados {DB_NAME} está criado!")
    # Except, trata a falha
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        connection.close()

    # Passando o flask para SQLAlchemy
    db.init_app(app=app)

    # Criando as tabelas a partir do model
    with app.test_request_context():
        db.create_all()

    # Inicializando a aplicação Flask
    app.run(host='0.0.0.0', port=4000, debug=True)
