from flask import render_template, request, redirect, url_for
import urllib # Envia requisições a uma URL
import json # Faz a conversão dos dados 

def init_app(app):
    
    # Lista em Python (array)
    players = ['Yan', 'Ferrari', 'Valéria', 'Amanda']
    gamelist = [{'Título': 'Need For Speed Most Wanted', 'Ano': '2005', 'Categoria': 'Corrida'}]
        
    @app.route('/')
    def home(): # Função que será executada ao acessar a rota
        return render_template('index.html')


    # Criando a rota '/games'
    @app.route('/games', methods=['GET','POST'])
    def games():
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        # Dicionário em Python (objeto)
        console = {'Nome' : 'Playstation 5',
                'Fabricante': 'Sony',
                'Ano': 2020}
        
        # Tratando uma requisição POST com Request
        if request.method == 'POST':
            # Coletando o texto da input
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))
        
        return render_template('games.html', 
                            title=title,
                            year=year,
                            category=category,
                            players=players,
                            console=console)

    @app.route('/newgame', methods=['GET','POST'])
    def newgame():
        
        # Tratando a requisição POST
        if request.method == 'POST':
            
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({'Titulo': request.form.get('title'), 'Ano' : request.form.get('year'), 'Categoria': request.form.get('category')})
                return redirect(url_for('newgame'))
                
        return render_template('newGame.html', gamelist=gamelist)
    
    @app.route('/apigames', methods=['GET', 'POST'])
    # Criando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET','POST'])
    def apigames(id=None): # Parâmetro opcional
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url)
        data = response.read()
        gamelist = json.loads(data)
        # Verificando se o parâmetro foi enviado
        if id:
            gameInfo = []
            for game in gamelist:
                if game['id'] == id: # Comparando os IDs
                    gameInfo = game
                    break
            if gameInfo:
                return render_template('gameinfo.html', gameInfo=gameInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:       
            return render_template ('apigames.html', gamelist=gamelist)
