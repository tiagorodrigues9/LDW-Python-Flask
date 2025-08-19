# Importando o flask
from flask import Flask, render_template
from controllers import routes
# Criando uma instância do Flask
app = Flask(__name__, template_folder='views') # __name__ representa o nome da aplicação que está sendo executada

routes.init_app(app)


# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    # Iniciando o servidor
    app.run(host='localhost', port=5000, debug=True)