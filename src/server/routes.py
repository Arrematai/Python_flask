from flask import Flask, json, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

## DATABASE
from src.infra.database.mysql import DataBase


## CONTROLLER
from src.domain.apis.controller import ApisController
from src.domain.leiloeiros.controller import LeiloeirosController
from src.domain.marcas.controller import MarcasController
from src.domain.modelos.controller import ModelosController
from src.domain.modelosAnos.controller import ModelosAnosController
from src.domain.fipes.controller import FipesController

def Routes(app: Flask, limiter: Limiter, database: DataBase):

  @app.route('/search', methods=['POST'])
  @limiter.limit("30000/day;5000/hour;500/minute")
  def search():
      try:
          apis = ApisController(request,get_remote_address())
          resultado = apis.exec()
          
          return jsonify(resultado)
      
      except Exception as e:
          print(e);
          return jsonify({"message": "API inválida"}), 200


  @app.route('/apis', methods=['GET'])
  @limiter.limit("1000/day;100/minute")
  def apis():
      apis = ["copart","palacio","sodresantoro","joaoemilio","superbid","rogeriomenezes","freitasleiloeiro", "liderleiloes", "pestanaleiloes", "vipleiloes", "guariglialeiloes", "ringolonleiloes"]
      return jsonify({"apis": apis}), 200

  ## FIPE
  ## Retorna todas as marcas
  @app.route('/fipe/marcas', methods=['GET'])
  @limiter.limit("1000/day;100/minute")
  def fipeMarcas():
      try:
          service = MarcasController(database)
          marcas = service.getMarcas()
          return jsonify({"data": { "success": True, "dados": marcas }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, }}), 200

  ## Retorna todos os modelos de uma marca
  @app.route('/fipe/marcas/<marcaID>/modelos', methods=['GET'])
  @limiter.limit("1000/day;100/minute")
  def fipeModelosByMarcaId(marcaID):
      try:
          if not marcaID:
              raise Exception("Marca deve ser enviada.") 
          service = ModelosController(database)
          modelos = service.getModelosByMarcaId(marcaID)
          return jsonify({"data": { "success": True, "dados": modelos }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, "message": e }}), 200

  # ## Retorna todos os anos de um modelo
  @app.route('/fipe/marcas/modelos/<modeloID>/anos', methods=['GET'])
  @limiter.limit("1000/day;100/minute")
  def fipeModelosAnosByModeloID(modeloID):
      try:
          if not modeloID:
              raise Exception("Modelo deve ser enviado.") 
          
          service = ModelosAnosController(database)
          modelos = service.getModelosByModeloId(modeloID)
          return jsonify({"data": { "success": True, "dados": modelos }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, "message": e }}), 200
      

  # ## Retorna os dados do carro
  @app.route('/fipe/marcas/<marcaID>/modelos/<modeloID>/anos/<ano>', methods=['GET'])
  @limiter.limit("1000/day;100/minute")
  def fipe(marcaID, modeloID,ano):
      try:
          if not marcaID:
              raise Exception("Marca deve ser enviado.") 
          if not modeloID:
              raise Exception("Modelo deve ser enviado.") 
          if not ano:
              raise Exception("Ano deve ser enviado.") 
          
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


  ## Leiloeiros
  @app.route('/leiloeiros', methods=['GET'])
  @limiter.limit("1000/day;10/minute")
  def getLeiloeiros():
      try:
          service = LeiloeirosController(database)
          leiloeiros = service.getLeiloeiros()
          return jsonify({"data": { "success": True, "dados": leiloeiros }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, }}), 200
      
  @app.route('/leiloeiros/list/estados', methods=['GET'])
  @limiter.limit("1000/day;10/minute")
  def getEstados():
      try:
          service = LeiloeirosController(database)
          estados = service.getEstados()
          return jsonify({"data": { "success": True, "dados": estados }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, }}), 200

  ## Leiloeiros By Estado
  @app.route('/leiloeiros/<estado>', methods=['GET'])
  @limiter.limit("1000/day;10/minute")
  def getLeiloeirosByEstado(estado):
      try:
          if not estado:
              raise Exception("Estado deve ser enviado.") 
          
          service = LeiloeirosController(database)
          leiloeiros = service.getLeiloeirosByEstado(estado)
          return jsonify({"data": { "success": True, "dados": leiloeiros }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, }}), 200
      
      
  ## Leiloeiros By Estado
  @app.route('/leiloeiros/<word_key>', methods=['GET'])
  @limiter.limit("1000/day;10/minute")
  def getLeiloeirosByWordKey(word_key):
      try:
          if not word_key:
              raise Exception("Estado deve ser enviado.") 
          
          service = LeiloeirosController(database)
          leiloeiros = service.getByWordKey(word_key)
          return jsonify({"data": { "success": True, "dados": leiloeiros }}), 200
      except Exception as e:
          return jsonify({"data": { "success": False, }}), 200



  @app.route('/online', methods=['GET'])
  def teste_online():
      return jsonify({"message": "API ONLINE"}), 200

  def init():
    print("Inicio Aplicação")
    context = ('fullchain.pem', 'privkey.pem')#certificate and key files
    app.run(host='0.0.0.0', port=5001, ssl_context=context)
    print("Aplicação Finalizada")
    
    
    