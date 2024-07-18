# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import ObjectId
import json

app = Flask(__name__)

# Configuração da conexão com o MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/seu_banco_de_dados"
mongo = PyMongo(app)

# Rota para listar todos os dados (GET)
@app.route('/dados', methods=['GET'])
def get_dados():
    dados = mongo.db.dados.find()
    result = []
    for dado in dados:
        result.append({'_id': str(dado['_id']), 'nome': dado['nome']})
    return jsonify(result)

# Rota para recuperar um dado específico por ID (GET)
@app.route('/dados/<string:dado_id>', methods=['GET'])
def get_dado(dado_id):
    dado = mongo.db.dados.find_one_or_404({'_id': ObjectId(dado_id)})
    return jsonify({'_id': str(dado['_id']), 'nome': dado['nome']})

# Rota para adicionar um novo dado (POST)
@app.route('/dados', methods=['POST'])
def add_dado():
    data = request.get_json()
    nome = data.get('nome', None)
    if nome:
        insert_result = mongo.db.dados.insert_one({'nome': nome})
        return jsonify({'mensagem': 'Dado adicionado com sucesso!', '_id': str(insert_result.inserted_id)}), 201
    else:
        return jsonify({'error': 'O campo "nome" é obrigatório'}), 400

# Rota para atualizar um dado existente por ID (PUT)
@app.route('/dados/<string:dado_id>', methods=['PUT'])
def update_dado(dado_id):
    data = request.get_json()
    nome = data.get('nome', None)
    if nome:
        update_result = mongo.db.dados.update_one({'_id': ObjectId(dado_id)}, {'$set': {'nome': nome}})
        if update_result.modified_count > 0:
            return jsonify({'mensagem': 'Dado atualizado com sucesso!'}), 200
        else:
            return jsonify({'error': 'Dado não encontrado'}), 404
    else:
        return jsonify({'error': 'O campo "nome" é obrigatório'}), 400

# Rota para deletar um dado por ID (DELETE)
@app.route('/dados/<string:dado_id>', methods=['DELETE'])
def delete_dado(dado_id):
    delete_result = mongo.db.dados.delete_one({'_id': ObjectId(dado_id)})
    if delete_result.deleted_count > 0:
        return jsonify({'mensagem': 'Dado deletado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Dado não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
