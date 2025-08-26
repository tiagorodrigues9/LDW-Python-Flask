from flask import render_template, request, redirect, url_for

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
