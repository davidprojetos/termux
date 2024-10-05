from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.route('/items/<int:item_id>')
def get_item(item_id):
    return jsonify({'item_id': item_id})

if __name__ == '__main__':
    app.run(debug=True)
