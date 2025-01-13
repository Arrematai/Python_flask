from flask import Flask, json, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


## DATABASE
from src.infra.database.mysql import DataBase

## CONTROLLER
from src.domain.apis.controller import ApisController
from src.domain.marcas.controller import MarcasController
from src.domain.modelos.controller import ModelosController
from src.domain.modelosAnos.controller import ModelosAnosController
from src.domain.fipes.controller import FipesController

# Lista de IPs/DNS a serem ignorados pelo limiter
IGNORED_IPS = {"127.0.0.1", "localhost", "https://arremataisolucoes.com.br", "https://arrematai.com.br"}

def custom_key_func():
    # Ignorar IPs específicos
    if get_remote_address() in IGNORED_IPS:
        return None
    # Para outros IPs, retornar o endereço IP
    return get_remote_address()

app = Flask(__name__)
limiter = Limiter(
    app=app,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri="memory://",
    key_func=custom_key_func
)
CORS(app, origins=["https://arremataisolucoes.com.br"],
supports_credentials=True, methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])

@app.route('/search', methods=['POST'])
def search():
    try:
        apis = ApisController(request,get_remote_address())
        resultado = apis.exec()
        
        return jsonify(resultado)
    
    except Exception as e:
        print(e);
        return jsonify({"message": "API inválida"}), 200


@app.route('/apis', methods=['GET'])
def apis():
    return jsonify({"apis": ["copart","palacio","sodresantoro","joaoemilio","superbid","rogeriomenezes","freitasleiloeiro"]}), 200

## FIPE
## Retorna todas as marcas
@app.route('/fipe/marcas', methods=['GET'])
def fipeMarcas():
    try:
        database = DataBase(dictionary=True)
        service = MarcasController(database)
        marcas = service.getMarcas()
        return jsonify({"data": { "success": True, "dados": marcas }}), 200
    except Exception as e:
        return jsonify({"data": { "success": False, }}), 200

## Retorna todos os modelos de uma marca
@app.route('/fipe/marcas/<marcaID>/modelos', methods=['GET'])
def fipeModelosByMarcaId(marcaID):
    try:
        if not marcaID:
            raise Exception("Marca deve ser enviada.") 
        database = DataBase(dictionary=True)
        service = ModelosController(database)
        modelos = service.getModelosByMarcaId(marcaID)
        return jsonify({"data": { "success": True, "dados": modelos }}), 200
    except Exception as e:
        return jsonify({"data": { "success": False, "message": e }}), 200

# ## Retorna todos os anos de um modelo
@app.route('/fipe/marcas/modelos/<modeloID>/anos', methods=['GET'])
def fipeModelosAnosByModeloID(modeloID):
    try:
        if not modeloID:
            raise Exception("Modelo deve ser enviado.") 
        
        database = DataBase(dictionary=True)
        service = ModelosAnosController(database)
        modelos = service.getModelosByModeloId(modeloID)
        return jsonify({"data": { "success": True, "dados": modelos }}), 200
    except Exception as e:
        return jsonify({"data": { "success": False, "message": e }}), 200
    

# ## Retorna os dados do carro
@app.route('/fipe/marcas/<marcaID>/modelos/<modeloID>/anos/<ano>', methods=['GET'])
def fipe(marcaID, modeloID,ano):
    try:
        if not marcaID:
            raise Exception("Marca deve ser enviado.") 
        if not modeloID:
            raise Exception("Modelo deve ser enviado.") 
        if not ano:
            raise Exception("Ano deve ser enviado.") 
        
        database = DataBase(dictionary=True)
        service = FipesController(database)
        carro = service.getCarro(marcaID, modeloID, ano)
        return jsonify({"data": { "success": True, "dados": carro }}), 200
    except Exception as e:
        return jsonify({"data": { "success": False, "message": e }}), 200

# ## Retorna os dados do carro
# @app.route('/fipe/marcas/<marcaID>/modelos/<modeloID>/anos/<ano>', methods=['GET'])
# def fipeCarro(marcaID, modeloID,ano):
#     try:
#         service = ServiceParallelum()
#         carro = service.getCarro(marcaID,modeloID,ano)
#         return jsonify({"data": { "success": True, "dados": carro }}), 200
#     except Exception as e:
#         return jsonify({"data": { "success": False, }}), 200
    

@app.route('/online', methods=['GET'])
def teste_online():
    return jsonify({"message": "API ONLINE"}), 200

def init():
  print("Inicio Aplicação")
#   context = ('fullchain.pem', 'privkey.pem')#certificate and key files
#   app.run(host='0.0.0.0', port=5001, ssl_context=context)
  app.run(host='0.0.0.0', port=5001)
  print("Aplicação Finalizada")