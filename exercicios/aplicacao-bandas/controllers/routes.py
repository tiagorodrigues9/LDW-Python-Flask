from flask import render_template, request, redirect, url_for

def init_app(app):
    
    musics = ['Be Quiet And Drive (Far Away)', 'My Own Summer (Shove It)', 'Change (In the house of flies)', 'Sextape', 'my mind is a mountain', 'i think about you all the time', 'Bloody Cape', 'Rats!Rats!Rats!']
    bandlist = [{'Banda': 'Deftones', 'Gênero': 'Metal Alternativo/Shoegaze', 'Criação': '1988', 'Música': 'Be Quiet And Drive (Far Away)', 'Membros': 'Chino Moreno, Stephen Carpenter, Abe Cunnigham, Frank Delgado, Fred Sablan'}]
    recomendations = ['Circle with me - Spiritbox', '5 Minutes Alone - Pantera', 'N.I.B - Black Sabbath', 'Gematria (The Killing Name) - Slipknot', 'Silvera - Gojira', 'Shadow Moses - Bring Me The Horizon', 'Them Bones - Alice In Chains', 'Emergence - Sleep Token','Clown - Korn', 'Given Up - Linkin Park', 'Lost In Translation - Sol Invicto']
        
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/bandas', methods=['GET','POST'])
    def bandas():
        band = 'Deftones'
        genre = 'Metal Alternativo/Shoegaze'
        yearCreation = '1988'
        members = [{'Nome' : 'Chino Moreno',
                'Função': 'Vocalista/Guitarrista'}, 
        {'Nome' : 'Stephen Carpenter', 'Função':'Guitarrista'},
        {'Nome': 'Abe Cunnigham', 'Função':'Baterista'},
        {'Nome': 'Frank Delgado', 'Função': 'DJ'},
        {'Nome': 'Fred Sablan', 'Função':'Baixista'}]
        
        
        if request.method == 'POST':
            if request.form.get('recomendation'):
                recomendations.append(request.form.get('recomendation'))
                return redirect(url_for('bandas'))
        
        return render_template('banda.html', 
                            band=band,
                            genre=genre,
                            yearCreation=yearCreation,
                            musics=musics,
                            members=members,
                            recomendations=recomendations)

    @app.route('/newbanda', methods=['GET','POST'])
    def newbanda():
        
        # Tratando a requisição POST
        if request.method == 'POST':
            
            if request.form.get('band') and request.form.get('genre') and request.form.get('yearCreation') and request.form.get('musics') and request.form.get('members'):
                bandlist.append({'Banda': request.form.get('band'), 'Gênero' : request.form.get('genre'), 'Criação': request.form.get('yearCreation'), 'Música': request.form.get('musics'), 'Membros': request.form.get('members')})
                return redirect(url_for('newbanda'))
                
        return render_template('newBanda.html', bandlist=bandlist)
