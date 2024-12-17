
from APIcopart import Copart
from APIpalacio import Palacio_dos_leiloes
from APIsodresantoro import SodreSantoro
from APIjoaoemilio import Joao_Emilio
from APIsuperbid import SuperBid
from APIrogeriomenezes import rogeriomenezes
from APIfreitas import Freitas


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app, origins=["https://arremataisolucoes.com.br"],
supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type", "Authorization"])

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    #colocar aqui paginação para carregamento mais rápido, modo assíncrono
    api = data.get('api')
    print(f"Query recebida: {query}")
    match api:
        case "copart":
            resultado = Copart(query) or [] 
        case "sodresantoro":
            resultado = SodreSantoro(query) or []
        case "palacio":
            resultado = Palacio_dos_leiloes(query)
        case "joaoemilio":
            resultado = Joao_Emilio(query) or []
        case "superbid":
            resultado = SuperBid(query) or []
        case "rogeriomenezes":
            resultado = rogeriomenezes(query) or []
        case "freitasleiloeiro":
            resultado = Freitas(query) or []
        case _:
            return jsonify({"message": "API inválida"}), 200
            

    return jsonify(resultado)


@app.route('/online', methods=['GET'])
def teste_online():
    
    return jsonify({"message": "API ONLINE"}), 500

@app.route('/apis', methods=['GET'])
def apis():
    
    return jsonify({"apis": ["copart","palacio","sodresantoro","joaoemilio","superbid","rogeriomenezes","freitasleiloeiro"]}), 200


if __name__ == '__main__':
    
    context = ('fullchain.pem', 'privkey.pem')#certificate and key files
    app.run(host='0.0.0.0', port=5000, ssl_context=context)

