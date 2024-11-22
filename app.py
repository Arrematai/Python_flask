
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


from APIcopart import Copart
from APIpalacio import Palacio_dos_leiloes
from APIsodresantoro import SodreSantoro
from APIjoaoemilio import Joao_Emilio
from APIsuperbid import SuperBid
from APIrogeriomenezes import Rogeriomenezes

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, origins=["https://arremataisolucoes.com.br"],
supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type", "Authorization"])

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')

    re_copart = Copart(query) or [] # Chama Copart e extrai o JSON
    re_sodre_santoro = SodreSantoro(query) or []
    re_palacio_dos_leiloes = Palacio_dos_leiloes(query) or []# Chama SodreSantoro e extrai o JSON
    re_joao_emilio = Joao_Emilio(query) or []
    re_superbid = SuperBid(query) or []
    re_rogerio_menezes = Rogeriomenezes(query) or []
    # # Mescla os resultados
    re_mesclados = re_copart + re_sodre_santoro + re_palacio_dos_leiloes + re_joao_emilio + re_superbid + re_rogerio_menezes

    random.shuffle(re_mesclados)
    
    # Retorna o JSON combinado
    return jsonify(re_mesclados)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

