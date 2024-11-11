# from flask import Flask, request, jsonify
# from APIcopart import Copart
# from APIsodresantoro import SodreSantoro
# from flask_cors import CORS
# import os

# app = Flask(__name__)
# CORS(app, origins=["https://www.arremataisolucoes.com.br"])

# @app.route('/search', methods=['POST'])
# def search():
#     data = request.json
#     query = data.get('query')

#     # Realiza as duas consultas
#     re_copart = Copart(query) or [] # Chama Copart e extrai o JSON
#     re_sodre_santoro = SodreSantoro(query) or []  # Chama SodreSantoro e extrai o JSON

#     # Mescla os resultados
#     re_mesclados = re_copart + re_sodre_santoro

#     # Retorna o JSON combinado
#     return jsonify(re_mesclados)



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from APIcopart import Copart
from APIsodresantoro import SodreSantoro
from APIpalacio import Palacio_dos_leiloes
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://www.arremataisolucoes.com.br"])

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')

    # Realiza as duas consultas
    re_copart = Copart(query) or [] # Chama Copart e extrai o JSON
    re_sodre_santoro = SodreSantoro(query) or []
    re_palacio_dos_leiloes = Palacio_dos_leiloes(query) or []# Chama SodreSantoro e extrai o JSON

    # Mescla os resultados
    re_mesclados = re_copart + re_sodre_santoro + re_palacio_dos_leiloes

    # Retorna o JSON combinado
    return jsonify(re_mesclados)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)