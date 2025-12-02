import time
import traceback

## INFRA
from src.infra.service.Logging import Log
from src.infra.helpers.importModules import dynamic_import

## DATABASE
from src.infra.database.mysql import DataBase

## APIS
from src.domain.apis.repository import ApisRepository
from src.domain.log.repository import LogsRepository


def init():
  print("Inicio Aplicação TESTE")
  log = Log("TESTE")
  # especifico = "freitasleiloeiro"
  # especifico = "receitafederal"
  especifico = "palacio"
  especifico = "copart"
  # especifico = "sodresantoro"
  # especifico = "mgl"
  # especifico = "pestanaleiloes"
  # especifico = "eleiloes"
  # especifico = "claudiokuss"
  query = "PORSCHE"
  # query = "bmw"
  resultados = []
  
  try:

    print(especifico)
    database = DataBase(dictionary=True)
    repository = ApisRepository(database)
    repositoryLog = LogsRepository(database)
        
    if especifico:
      start_time = time.time()
      api = repository.getApi(especifico)

      if api:
        ServiceClass  = dynamic_import(api["path"], api["class"], api["nome"]) 
        # Verifica se a classe foi carregada corretamente e instancia um objeto
        if ServiceClass:
          instance = ServiceClass(query, 2000)  # Instancia a classe
          response = instance.exec()
          resultados = response["resultados"] or []
          print(resultados)
          # print(len(resultados))
          end_time = time.time()
          log.executionTime(query=query, api=especifico,end=end_time, start=start_time, resultados=len(resultados))
          repositoryLog.insertApis({
            "ip": "TESTE",
            "api": api["nome"],
            "query": query,
            "duration": end_time - start_time,
            "http_code": response["http_code"],
            "results": len(resultados)
          })
    else:    
      dados = repository.getApis()
      for api in dados:
          
          print(api)
          start_time = time.time()
      
          ServiceClass  = dynamic_import(api["path"], api["class"]) 
          # Verifica se a classe foi carregada corretamente e instancia um objeto
          if ServiceClass:
            instance = ServiceClass(query, 2000)  # Instancia a classe
            response = instance.exec()
            resultados = response["resultados"] or []
            # print(result)
            print(len(resultados))
            end_time = time.time()
            log.executionTime(query=query, api=especifico,end=end_time, start=start_time, resultados=len(resultados))
            repositoryLog.insertApis({
              "ip": "TESTE",
              "api": api["nome"],
              "query": query,
              "duration": end_time - start_time,
              "http_code": response["http_code"],
              "results": len(resultados)
            })


        
  except Exception as e:
      print(f"Error: {e}")
      traceback.print_exc()  # <-- Mostra o traceback completo no terminal
  


  print("Aplicação Finalizada TESTE")