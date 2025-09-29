from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Banda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    genero = db.Column(db.String(150))
    ano_criacao = db.Column(db.Integer)

    def __init__(self, nome, genero, ano_criacao):
        self.nome = nome
        self.genero = genero
        self.ano_criacao = ano_criacao

class Musica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    ano_lancamento = db.Column(db.Integer)
    album = db.Column(db.String(150))
    tempo = db.Column(db.Integer)
    banda_id = db.Column(db.Integer, db.ForeignKey('banda.id'))

    # Definindo o relacionamento
    banda = db.relationship('Banda', backref=db.backref('musica', lazy=True))

    def __init__(self, titulo, ano_lancamento, album, tempo ,banda_id):
        self.titulo = titulo
        self.ano_lancamento = ano_lancamento
        self.album = album
        self.tempo = tempo
        self.banda_id = banda_id
