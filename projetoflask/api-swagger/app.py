from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Swagger Configuração
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Flask API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Criando uma tabela no banco de dados
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'<Item {self.name}>'

# Criação da tabela no banco de dados
with app.app_context():
    db.create_all()

# Definindo o Recurso da API
class ItemResource(Resource):
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return jsonify({"id": item.id, "name": item.name, "description": item.description})

    def post(self):
        data = request.get_json()
        new_item = Item(name=data['name'], description=data['description'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item created", "id": new_item.id})

    def put(self, item_id):
        data = request.get_json()
        item = Item.query.get_or_404(item_id)
        item.name = data['name']
        item.description = data['description']
        db.session.commit()
        return jsonify({"message": "Item updated"})

    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"})

# Inicializando a API e adicionando os Recursos
api = Api(app)
api.add_resource(ItemResource, '/item', '/item/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)

