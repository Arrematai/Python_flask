from flask import Request
import time
from flask_restful import Resource

## INFRA
from src.infra.service.Logging import Log
from src.infra.helpers.importModules import dynamic_import

## DATABASE
from src.infra.database.mysql import DataBase

## APIS
from src.domain.apis.repository import ApisRepository
from src.domain.log.repository import LogsRepository

class ApisController(Resource):
    
  def __init__(self, request: Request, ip: str,database: DataBase):
    self.request = request
    self.Log = Log(ip)
    self.database = database
    self.ip = ip
    
  def getApis(self):
    try:
      repository = ApisRepository(self.database)
      
      apis = repository.getApis()
      
      return [api['nome'] for api in apis]
    except Exception as e:
      print("Error APIS", e)
      raise Exception("Apis não encontrada.")
    
  
  def exec(self):
    try:
      data = self.request.json
      query = data.get('query')
      api = data.get('api')
      print(f"Query recebida: {query}")
      print(f"Api recebida: {api}")

      start_time = time.time()
      resultados = []
      currApi = None
      
      repository = ApisRepository(self.database)
      repositoryLog = LogsRepository(self.database)
      
      if api:
          currApi = repository.getApi(api)
          if currApi:
              ServiceClass  = dynamic_import(currApi["path"], currApi["class"]) 
              # Verifica se a classe foi carregada corretamente e instancia um objeto
              if ServiceClass:
                  instance = ServiceClass(query, 2000, currApi["nome"])  # Instancia a classe
                  response = instance.exec()

                  resultados = response["resultados"] or []
              else:
                  raise Exception("ServiceClass não foi executada.")
          else:
              raise Exception("Dado não encontrada.")
      else:
          raise Exception("Api não enviada.")
      
              
      end_time = time.time()

      ## LOG REGISTER
      self.Log.executionTime(query=query, api=api,end=end_time, start=start_time, resultados=len(resultados))
      repositoryLog.insertApis({
         "ip": self.ip,
         "api": currApi["nome"] or None,
         "query": query,
         "duration": end_time - start_time,
         "http_code": response["http_code"],
         "results": len(resultados)
      })
      return resultados
    except Exception as e:
      print("Error API", e)
      raise Exception("Api não encontrada.")