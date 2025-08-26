from flask import render_template, request, redirect, url_for

def init_app(app):
    
    musics = ['Be Quiet And Drive (Far Away)', 'My Own Summer (Shove It)', 'Change (In the house of flies)', 'Sextape']
    gamelist = [{'Título': 'Need For Speed Most Wanted', 'Ano': '2005', 'Categoria': 'Corrida'}]
        
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/bandas', methods=['GET','POST'])
    def bandas():
        band = 'Deftones'
        gender = 'Metal Alternativo/Shoegaze'
        yearCreation = '1988'
        members = [{'Nome' : 'Chino Moreno',
                'Função': 'Vocalista/Guitarrista'}, 
        {'Nome' : 'Stephen Carpenter', 'Função':'Guitarrista'},
        {'Nome': 'Abe Cunnigham', 'Função':'Baterista'},
        {'Nome': 'Frank Delgado', 'Função': 'DJ'},
        {'Nome': 'Fred Sablan', 'Função':'Baixista'}]
        
        
        # Tratando uma requisição POST com Request
        if request.method == 'POST':
            # Coletando o texto da input
            if request.form.get('music'):
                musics.append(request.form.get('music'))
                return redirect(url_for('bandas'))
        
        return render_template('banda.html', 
                            band=band,
                            gender=gender,
                            yearCreation=yearCreation,
                            musics=musics,
                            members=members)

    @app.route('/newbanda', methods=['GET','POST'])
    def newbanda():
        
        # Tratando a requisição POST
        if request.method == 'POST':
            
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({'Titulo': request.form.get('title'), 'Ano' : request.form.get('year'), 'Categoria': request.form.get('category')})
                return redirect(url_for('newgame'))
                
        return render_template('newGame.html', gamelist=gamelist)
