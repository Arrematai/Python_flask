from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from src.services.copart import ServiceCopart
from src.services.sodresantoro import ServiceSantoro
from src.services.freitas import ServiceFreitas
from src.services.palacio import ServicePalacios
from src.services.superbid import ServiceSuperBid
from src.services.joaoemilionew import ServiceJoaoEmilio 

app = Flask(__name__)
CORS(app, origins=["https://arremataisolucoes.com.br"],
supports_credentials=True, methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    api = data.get('api')
    print(f"Query recebida: {query}")
    match api:
        case "copart":
            copart = ServiceCopart(query,"2000")
            resultado = copart.exec() or [] 
        case "sodresantoro":
            santoro = ServiceSantoro(query,"2000")
            resultado = santoro.exec() or []
        case "palacio":
            palacios = ServicePalacios(query,"2000")
            resultado = palacios.exec()
        case "joaoemilio":
            joaoEmilio = ServiceJoaoEmilio("fiat","2000")
            resultado = joaoEmilio.exec() or []
        case "superbid":
            superbid = ServiceSuperBid(query,"2000")
            resultado = superbid.exec() or []
        case "freitasleiloeiro":
            freitas = ServiceFreitas(query,"2000")
            resultado = freitas.exec() or []
        case "rogeriomenezes":
            resultado = rogeriomenezes(query) or []
        case _:
            return jsonify({"message": "API inválida"}), 200
            

    return jsonify(resultado)

@app.route('/apis', methods=['GET'])
def apis():
    return jsonify({"apis": ["copart","palacio","sodresantoro","joaoemilio","superbid","rogeriomenezes","freitasleiloeiro"]}), 200

@app.route('/online', methods=['GET'])
def teste_online():
    return jsonify({"message": "API ONLINE"}), 200

def init():
  print("Inicio Aplicação")
  context = ('fullchain.pem', 'privkey.pem')#certificate and key files
  app.run(host='0.0.0.0', port=6000, ssl_context=context)
#   app.run(host='0.0.0.0', port=6000)
  print("Aplicação Finalizada")