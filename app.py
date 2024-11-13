from flask import Flask, request, jsonify
from APIjoaoemilio import Joao_Emilio
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://www.arremataisolucoes.com.br"], supports_credentials=True)


@app.route('/test_joao_emilio', methods=['POST', 'OPTIONS'])
def test_joao_emilio():
    if request.method == 'OPTIONS':
        # Responde a requisições OPTIONS com status 200
        response = jsonify({"status": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "https://www.arremataisolucoes.com.br")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    # Processa a requisição POST
    data = request.json
    query = data.get('query')
    re_joao_emilio = Joao_Emilio(query) or []
    response = jsonify(re_joao_emilio)
    response.headers.add("Access-Control-Allow-Origin", "https://www.arremataisolucoes.com.br")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






# from flask import Flask, request, jsonify
# from APIcopart import Copart
# from APIpalacio import Palacio_dos_leiloes
# from APIsodresantoro import SodreSantoro
# from APIjoaoemilio import Joao_Emilio
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins=["https://www.arremataisolucoes.com.br"])

# @app.route('/search', methods=['POST'])
# def search():
#     data = request.json
#     query = data.get('query')

#     # Realiza as duas consultas
#     re_copart = Copart(query) or [] # Chama Copart e extrai o JSON
#     re_sodre_santoro = SodreSantoro(query) or []
#     re_palacio_dos_leiloes = Palacio_dos_leiloes(query) or []# Chama SodreSantoro e extrai o JSON
#     re_joao_emilio = Joao_Emilio(query) or []

#     # Mescla os resultados
#     re_mesclados = re_copart + re_sodre_santoro + re_palacio_dos_leiloes + re_joao_emilio
#     print(re_joao_emilio)

#     # Retorna o JSON combinado
#     return jsonify(re_mesclados)



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

