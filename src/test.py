import time

## INFRA
from src.infra.service.Logging import Log
from src.infra.helpers.importModules import dynamic_import

## DATABASE
from src.infra.database.mysql import DataBase

## APIS
from src.domain.apis.repository import ApisRepository
from src.domain.apis.services.kuss import ServiceKuss
# from src.domain.apis.services.mgl import ServiceMgl


## WORDKEY
from src.domain.leiloeiros.controller import LeiloeirosController


def init():
  print("Inicio Aplicação TESTE")
  start_time = time.time()
  log = Log("TESTE")
  especifico = "topoleiloes"
  result = None
  
  try:
    
    mgl = ServiceKuss("fiat", 2000)
    result = mgl.exec()
    
    # database = DataBase(dictionary=True)
    # repository = ApisRepository(database)
    
    # if especifico:
    #   api = repository.getApi(especifico)
      
    #   print(api)

    #   if api:
    #     ServiceClass  = dynamic_import(api["path"], api["class"]) 
    #     # Verifica se a classe foi carregada corretamente e instancia um objeto
    #     if ServiceClass:
    #       instance = ServiceClass("fiat", 2000)  # Instancia a classe
    #       result = instance.exec() or []
    # else:    
    #   dados = repository.getApis()
    #   for api in dados:
      
    #       ServiceClass  = dynamic_import(api["path"], api["class"]) 
    #       # Verifica se a classe foi carregada corretamente e instancia um objeto
    #       if ServiceClass:
    #         instance = ServiceClass("fiat", 2000)  # Instancia a classe
    #         result = instance.exec() or []
      

        
  except Exception as e:
      print(f"Error: {e}")
  

  print("Resultados:",len(result))
  end_time = time.time()
  log.executionTime(query="fiat", api="TESTE",end=end_time, start=start_time)
  print("Aplicação Finalizada TESTE")