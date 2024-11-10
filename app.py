from flask import Flask, request, jsonify
from APIcopart import Copart

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')  # Recebe a query enviada pelo cliente
    return Copart(query)       # Retorna a resposta da função como JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
