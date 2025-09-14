from flask import render_template, request, redirect, url_for, jsonify
import requests   # Para fazer requisições HTTP às APIs
import time  # Para pausas e controle de tempo
import json  # Para trabalhar com arquivos JSON
import os  # Para operações com arquivos e pastas
from datetime import datetime, timedelta # Para datas e horários
from concurrent.futures import ThreadPoolExecutor, as_completed # Para processamento paralelo de coleta de informações na API
from functools import lru_cache # Para cache de funções

def init_app(app):
    
    musics = ['Be Quiet And Drive (Far Away)', 'My Own Summer (Shove It)', 'Change (In the house of flies)', 'Sextape', 'my mind is a mountain', 'i think about you all the time', 'Bloody Cape', 'Rats!Rats!Rats!']
    bandlist = [{'Banda': 'Deftones', 'Gênero': 'Metal Alternativo/Shoegaze', 'Criação': '1988', 'Música': 'Be Quiet And Drive (Far Away)', 'Membros': 'Chino Moreno, Stephen Carpenter, Abe Cunnigham, Frank Delgado, Fred Sablan'}]
    recomendations = ['Circle with me - Spiritbox', '5 Minutes Alone - Pantera', 'N.I.B - Black Sabbath', 'Gematria (The Killing Name) - Slipknot', 'Silvera - Gojira', 'Shadow Moses - Bring Me The Horizon', 'Them Bones - Alice In Chains', 'Emergence - Sleep Token','Clown - Korn', 'Given Up - Linkin Park', 'Lost In Translation - Sol Invicto']
    catalog_bands = ["Deftones", "Slipknot", "Metallica", "Black Sabbath","Ozzy Osbourne", "Spiritbox", "Gojira", "Bring Me The Horizon", "Korn", "Linkin Park","Sleep Token", "Alice In Chains", "Pantera", "Tool", "System of a Down", "Rammstein", "Lamb of God", "Avenged Sevenfold", "Trivium", "Dream Theater", "Disturbed", "Chevelle", "Meshuggah", "Killswitch Engage", "Creed", "Soundgarden", "Team Sleep"] # Lista de bandas para o catálogo. A lista é necessária para fazer a consulta nas APIs.
    # Variáveis para controle do token do Spotify
    SPOTIFY_ACCESS_TOKEN = None  # Armazena o token de acesso
    SPOTIFY_TOKEN_EXPIRY = None # Armazena quando o token expira
    CACHE_FILE = "bandas_cache.json" # Arquivo onde os dados são salvos
    CACHE_DURATION = 3600 # Tempo que o cache vale (1 hora em segundos)
    
        
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
        
        if request.method == 'POST':
            
            if request.form.get('band') and request.form.get('genre') and request.form.get('yearCreation') and request.form.get('musics') and request.form.get('members'):
                bandlist.append({'Banda': request.form.get('band'), 'Gênero' : request.form.get('genre'), 'Criação': request.form.get('yearCreation'), 'Música': request.form.get('musics'), 'Membros': request.form.get('members')})
                return redirect(url_for('newbanda'))
                
        return render_template('newBanda.html', bandlist=bandlist)
    
    def get_spotify_token(): # Gera um novo token de acesso para a API do Spotify
        nonlocal SPOTIFY_ACCESS_TOKEN, SPOTIFY_TOKEN_EXPIRY
        
        auth_url = 'https://accounts.spotify.com/api/token'
        # auth_data = {
        #     'grant_type': 'client_credentials',
        #     'client_id': 'e0578467850d4d39adeee53dee3e9733', # A chave da API
        #     'client_secret': 'eb430c583092414789506f04c802927b', # O segredo da API
        # } Precisa descomentar essa linha para funcionar
        
        try: # Faz a requisição para obter o token
            auth_response = requests.post(auth_url, data=auth_data) # Envia uma solicitação POST para o servidor do Spotify. O Spotify responde com informações que ficam armazenadas em auth_response
            auth_response.raise_for_status() # Verifica se a requisição foi bem-sucedida, ajuda a evitar que o programa continue se a autenticação falhar
            token_data = auth_response.json() # Converte a resposta em JSON para um dicionário Python
            
            SPOTIFY_ACCESS_TOKEN = token_data['access_token'] # Pega o token de acesso da resposta do Spotify
            expires_in = token_data['expires_in'] # Pega o tempo de expiração do token
            SPOTIFY_TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in) # Calcula a data/hora exata em que o token expira
            
            print("Novo token do Spotify gerado com sucesso.")
            print(f"Token expira em: {SPOTIFY_TOKEN_EXPIRY}")
            return SPOTIFY_ACCESS_TOKEN
            
        except requests.exceptions.RequestException as e: # Captura erros que podem acontecer na requisição HTTP
            print(f"❌ Erro ao gerar token do Spotify: {e}")
            return None
        
    def refresh_token_if_needed():
        nonlocal SPOTIFY_ACCESS_TOKEN, SPOTIFY_TOKEN_EXPIRY
        
        # Se não tem token OU token expirado (ou expira em menos de 30 segundos)
        if (SPOTIFY_ACCESS_TOKEN is None or 
            SPOTIFY_TOKEN_EXPIRY is None or 
            datetime.now() > SPOTIFY_TOKEN_EXPIRY - timedelta(seconds=30)):
            
            print("🔄 Token expirado ou prestes a expirar. Gerando novo...")
            return get_spotify_token()
        else:
            # Calcula quanto tempo ainda falta para o token expirar
            time_left = SPOTIFY_TOKEN_EXPIRY - datetime.now()
            print(f"✅ Token válido. Expira em: {int(time_left.total_seconds())} segundos")
            return SPOTIFY_ACCESS_TOKEN

    
    def fetch_band_data(band_name):
        """Busca TODOS os dados de uma banda das APIs (MusicBrainz + Spotify)"""
        
        # 1. Busca dados textuais no MusicBrainz
        mb_data = fetch_musicbrainz_data(band_name)
        if not mb_data:
            return None
        
        # 2. Busca imagem e música popular no Spotify
        spotify_data = fetch_spotify_data(band_name)
        
        # Combina todos os dados
        return {**mb_data, **spotify_data}
    
    def get_wikipedia_description(band_name):
        """Busca descrição da banda na Wikipedia em Português"""
        try:
            # Formata o nome para URL (ex: "Deftones" → "Deftones")
            formatted_name = band_name.replace(" ", "_")
            
            # API da Wikipedia em Português
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{formatted_name}"
            
            headers = {'User-Agent': 'MeuCatalogoMetal/1.0 (seu_email@gmail.com)'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                description = data.get("extract", "")
                
                # Se não encontrou em português, tenta em inglês
                if not description or "pode referir-se a:" in description:
                    url_en = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_name}"
                    response_en = requests.get(url_en, headers=headers, timeout=10)
                    
                    if response_en.status_code == 200:
                        data_en = response_en.json()
                        description = data_en.get("extract", "")
                
                # Limita o tamanho da descrição
                if len(description) > 500:
                    description = description[:500] + "..."
                    
                return description if description else "Descrição não disponível."
            
            return "Descrição não disponível."
            
        except Exception as e:
            print(f"Erro ao buscar Wikipedia para {band_name}: {e}")
            return "Descrição não disponível."

    def fetch_musicbrainz_data(band_name):
        """Busca dados da banda no MusicBrainz - SOLUÇÃO DEFINITIVA"""
        headers = {'User-Agent': 'MeuCatalogoMetal/1.0 (seu_email@gmail.com)'}
        
        try:
            # PRIMEIRA CHAMADA: Busca o artista principal
            search_url = "https://musicbrainz.org/ws/2/artist/"
            search_params = {
                "query": f'artist:"{band_name}"',
                "fmt": "json"
            }
            
            search_response = requests.get(search_url, params=search_params, headers=headers)
            search_response.raise_for_status()
            search_data = search_response.json()

            if not search_data.get("artists"):
                return None

            artist = search_data["artists"][0]
            artist_id = artist.get("id")
            
            # SEGUNDA CHAMADA: Busca relações usando o ID do artista
            relations_url = f"https://musicbrainz.org/ws/2/artist/{artist_id}"
            relations_params = {
                "fmt": "json",
                "inc": "artist-rels"  # Agora VAI funcionar!
            }
            
            relations_response = requests.get(relations_url, params=relations_params, headers=headers)
            relations_response.raise_for_status()
            relations_data = relations_response.json()
            
            # Extrai os membros
            members = []
            if "relations" in relations_data:
                for rel in relations_data["relations"]:
                    if (rel.get("type") in ["member", "member of band", "current member", "founder"] and
                        rel.get("artist") and
                        rel["artist"].get("type") == "Person"):
                        
                        member_name = rel["artist"]["name"]
                        if member_name not in members:
                            members.append(member_name)

            # Extrair ano de criação
            creation_year = "N/A"
            if "life-span" in artist and artist["life-span"].get("begin"):
                begin_date = artist["life-span"]["begin"]
                creation_year = begin_date.split("-")[0] if begin_date else "N/A"

            # Extrair gênero das tags (da primeira resposta)
            genre = "Metal"
            if "tags" in artist and artist["tags"]:
                most_popular_tag = max(artist["tags"], key=lambda x: x.get("count", 0))
                genre = most_popular_tag["name"].title()

            # 🔥 AGORA COM DESCRIÇÃO DA WIKIPEDIA
            wikipedia_description = get_wikipedia_description(band_name)
            
            return {
                "nome": artist.get("name", band_name),
                "genero": genre,
                "criacao": creation_year,
                "membros": ", ".join(members) if members else "Membros não encontrados",
                "descricao": wikipedia_description  # ✅ Descrição da Wikipedia
            }
            
        except Exception as e:
            print(f"Erro ao acessar MusicBrainz para {band_name}: {e}")
            return None

    def fetch_spotify_data(band_name):
        """Busca imagem e música popular no Spotify - VERSÃO OTIMIZADA"""
        # Verifica token UMA vez por requisição
        token = refresh_token_if_needed()
        if not token:
            print(f"❌ Não foi possível obter token para {band_name}")
            return {"image_url": None, "popular_track": None, "spotify_url": None}
        
        headers = {'Authorization': f'Bearer {token}'}
        search_url = 'https://api.spotify.com/v1/search'
        params = {
            'q': band_name,
            'type': 'artist',
            'limit': 1
        }
        
        try:
            # Busca o artista
            response = requests.get(search_url, params=params, headers=headers)
            
            # Se token inválido (raro, pois já verificamos acima)
            if response.status_code == 401:
                print("🔄 Token inválido. Gerando novo e tentando novamente...")
                token = get_spotify_token()  # Gera novo token FORÇADAMENTE
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(search_url, params=params, headers=headers)
                response.raise_for_status()
            
            response.raise_for_status()
            artist_data = response.json().get('artists', {}).get('items', [])
            
            if not artist_data:
                print(f"⚠️  Artista {band_name} não encontrado no Spotify")
                return {"image_url": None, "popular_track": None, "spotify_url": None}
            
            artist = artist_data[0]
            image_url = artist['images'][0]['url'] if artist.get('images') else None
            
            # Busca músicas mais populares
            tracks_url = f"https://api.spotify.com/v1/artists/{artist['id']}/top-tracks"
            tracks_params = {'market': 'BR'}
            tracks_response = requests.get(tracks_url, params=tracks_params, headers=headers)
            tracks_response.raise_for_status()
            tracks_data = tracks_response.json().get('tracks', [])
            
            popular_track = tracks_data[0]['name'] if tracks_data else "Nenhuma música encontrada"
            spotify_url = tracks_data[0]['external_urls']['spotify'] if tracks_data else "https://open.spotify.com"
            
            print(f"✅ Dados do Spotify obtidos para {band_name}")
            return {
                "image_url": image_url,
                "popular_track": popular_track,
                "spotify_url": spotify_url
            }
            
        except Exception as e:
            print(f"❌ Erro ao acessar Spotify para {band_name}: {e}")
            return {"image_url": None, "popular_track": None, "spotify_url": None}

    def load_cache():
        """Carrega os dados do cache se existirem e estiverem válidos"""
        if not os.path.exists(CACHE_FILE):
            return None
            
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # Verifica se o cache ainda é válido
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            time_diff = (datetime.now() - cache_time).total_seconds()
            
            if time_diff < CACHE_DURATION:
                print("✅ Usando cache válido")
                return cache_data['bandas']
            else:
                print("⚠️ Cache expirado")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao carregar cache: {e}")
            return None
    
    def save_cache(bandas_data):
        """Salva os dados no cache"""
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'bandas': bandas_data
            }
            
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
            print("💾 Cache salvo com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao salvar cache: {e}")

    # --- ROTAS PRINCIPAIS ---
    @app.route('/catalogo', methods=['GET','POST'])
    def catalogo():
        """Página principal com CACHE INTELIGENTE"""
        # Primeiro tenta carregar do cache
        cached_bandas = load_cache()
        
        if cached_bandas:
            print("🚀 Retornando dados do cache (super rápido!)")
            return render_template('catalogo.html', bandas=cached_bandas)
        
        # Se não tem cache ou expirou, busca das APIs
        print("🔍 Buscando dados das APIs...")
        bandas_data = []
        
        for i, band_name in enumerate(catalog_bands):
            try:
                print(f"📡 Consultando {band_name} ({i + 1}/{len(catalog_bands)})")
                
                data = fetch_band_data(band_name)
                if data:
                    bandas_data.append({
                        'nome': data['nome'],
                        'genero': data['genero'],
                        'image_url': data['image_url']
                    })
                    print(f"✅ {band_name} - Sucesso")
                else:
                    print(f"❌ {band_name} - Falha")
                
                # Delay menor já que é apenas na primeira vez
                if i < len(catalog_bands) - 1:
                    time.sleep(0.5)  # Apenas 500ms
                    
            except Exception as e:
                print(f"❌ Erro em {band_name}: {e}")
                continue
        
        # Salva no cache para as próximas vezes
        save_cache(bandas_data)
        
        return render_template('catalogo.html', bandas=bandas_data)

    @app.route('/detalhes/<band_name>', methods=['GET','POST'])
    def detalhes_banda(band_name):
        """Página de detalhes também com cache"""
        # Para detalhes, podemos usar um cache separado ou buscar sempre
        # Vou fazer uma versão simples que busca sempre
        banda_data = fetch_band_data(band_name)
        
        if not banda_data:
            return "Banda não encontrada", 404
        
        return render_template('detalhes_banda.html', banda=banda_data)
