from flask import render_template

def init_app(app):
    @app.route('/')
    def home(): # Função que será executada ao acessar a rota
        return render_template('index.html')


    # Criando a rota '/games'
    @app.route('/games')
    def games():
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        # Lista em Python (array)
        players = ['Yan', 'Ferrari', 'Valéria', 'Amanda']
        # Dicionário em Python (objeto)
        console = {'Nome' : 'Playstation 5',
                'Fabricante': 'Sony',
                'Ano': 2020}
        return render_template('games.html', 
                            title=title,
                            year=year,
                            category=category,
                            players=players,
                            console=console)
