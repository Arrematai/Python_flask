
from APIcopart import Copart
from APIpalacio import Palacio_dos_leiloes
from APIsodresantoro import SodreSantoro
from APIjoaoemilio import Joao_Emilio
from APIsuperbid import SuperBid
from APIrogeriomenezes import rogeriomenezes
from DadosML import SaveML

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
    if api=="Copart":
        re_copart = Copart(query) or []

    re_sodre_santoro = SodreSantoro(query) or []
    re_palacio_dos_leiloes = Palacio_dos_leiloes(query) or []# Chama SodreSantoro e extrai o JSON
    re_joao_emilio = Joao_Emilio(query) or []
    re_superbid = SuperBid(query) or []
    re_rogerio_menezes = rogeriomenezes(query) or []
    # # Mescla os resultados
    re_mesclados = re_copart + re_sodre_santoro + re_palacio_dos_leiloes + re_joao_emilio + re_rogerio_menezes

    random.shuffle(re_mesclados)
    SaveML(re_mesclados, "BDML.json")


        
    # Retorna o JSON combinado
    return jsonify(re_mesclados)


@app.route('/download', methods=['GET'])
def download_dados():
    """
    Endpoint para download do arquivo de treinamento.
    """
    arquivo_saida = "BDML.json"  
    try:
        return send_file(arquivo_saida, as_attachment=True)
    except FileNotFoundError:
        return "Arquivo não encontrado", 404


@app.route('/delete', methods=['DELETE'])
def delete_dados():
    """
    Endpoint para deletar o arquivo de treinamento.
    """
    arquivo_saida = "BDML.json"  # Nome do arquivo salvo
    try:
        if os.path.exists(arquivo_saida):
            os.remove(arquivo_saida)  # Remove o arquivo
            return jsonify({"message": "Arquivo de treinamento deletado com sucesso."}), 200
        else:
            return jsonify({"message": "Arquivo não encontrado."}), 404
    except Exception as e:
        return jsonify({"message": f"Erro ao deletar o arquivo: {str(e)}"}), 500

@app.route('/online', methods=['GET'])
def teste_online():
    
    return jsonify({"message": "API ONLINE"}), 500

@app.route('/apis', methods=['GET'])
def apis():
    
    return jsonify({"apis": ["copart","palacio","sodresantoro","joaoemilio","superbid","rogeriomenezes"]}), 500


if __name__ == '__main__':
    
    context = ('fullchain.pem', 'privkey.pem')#certificate and key files
    app.run(host='0.0.0.0', port=5000, ssl_context=context)

