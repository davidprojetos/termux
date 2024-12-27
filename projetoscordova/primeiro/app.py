from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para o usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Inicializar banco de dados
with app.app_context():
    db.create_all()

# Rota para cadastrar usuários
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    if not nome or not email or not senha:
        return jsonify({'erro': 'Preencha todos os campos!'}), 400

    # Verifica se o email já existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'erro': 'Email já cadastrado!'}), 400

    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'}), 201

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({'erro': 'Preencha todos os campos!'}), 400

    # Verifica credenciais
    usuario = Usuario.query.filter_by(email=email, senha=senha).first()
    if usuario:
        return jsonify({'mensagem': f'Bem-vindo, {usuario.nome}!'}), 200
    else:
        return jsonify({'erro': 'Email ou senha inválidos!'}), 401

if __name__ == '__main__':
    app.run(debug=True)
