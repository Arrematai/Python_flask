from flask import Flask, request, jsonify
from APIcopart import Copart
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://www.arremataisolucoes.com.br"])

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')  # Recebe a query enviada pelo cliente
    return Copart(query)       # Retorna a resposta da função como JSON

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=5000)

# from flask import Flask, request, jsonify
# from APIcopart import Copart
# from APIsodresantoro import SodreSantoro

# app = Flask(__name__)

# @app.route('/search', methods=['POST'])
# def search():
#     data = request.json
#     query = data.get('query')

#     # Realiza as duas consultas
#     re_copart = Copart(query).json  # Chama Copart e extrai o JSON
#     re_sodre_santoro = SodreSantoro(query).json  # Chama SodreSantoro e extrai o JSON

#     # Mescla os resultados
#     re_mesclados = re_copart + re_sodre_santoro

#     # Retorna o JSON combinado
#     return jsonify(re_mesclados)



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
