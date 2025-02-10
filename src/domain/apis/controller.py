from flask import Request
import time
from flask_restful import Resource

## INFRA
from src.infra.service.Logging import Log
from src.infra.helpers.importModules import dynamic_import

## DATABASE
from src.infra.database.mysql import DataBase

## REPOSITORY
from src.domain.apis.repository import ApisRepository
from src.domain.apis.LocalRepository import obter_apis


class ApisController(Resource):
    
  def __init__(self, request: Request, ip: str,database: DataBase):
    self.request = request
    self.Log = Log(ip)
    self.database = database
    
  def getApis(self):
    repository = ApisRepository(self.database)
    apis = repository.getApis()
    
    return [api['nome'] for api in apis]
    
  
  def exec(self):
    try:
      data = self.request.json
      query = data.get('query')
      api = data.get('api')
      print(f"Query recebida: {query}")
      print(f"Api recebida: {api}")
      start_time = time.time()
      resultados = []
      
      if api:
          APIS = obter_apis()

          API = next((item for item in APIS if item['nome'] == api), None)

          if not API:
            raise Exception("Api não encontrada.")

          if API and API["ativo"] == 1 and API["status_site"]:
              ServiceClass  = dynamic_import(API["path"], API["class"]) 
              # Verifica se a classe foi carregada corretamente e instancia um objeto
              if ServiceClass:
                  instance = ServiceClass(query, 2000)  # Instancia a classe
                  resultados = instance.exec() or []
              else:
                  raise Exception("ServiceClass não foi executada.")
          else:
              raise Exception("Dado não encontrada ou não está ativo ou dite down.")
      else:
          raise Exception("Api não enviada.")
      

      
              
      end_time = time.time()
      self.Log.executionTime(query=query, api=api,end=end_time, start=start_time)
      return resultados
    except Exception as e:
      print("Error APIS", e)
      raise Exception("erro geral na apis.")