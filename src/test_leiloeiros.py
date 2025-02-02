import time

## INFRA
from src.infra.service.Logging import Log

## DATABASE
from src.infra.database.mysql import DataBase

## WORDKEY
from src.domain.leiloeiros.controller import LeiloeirosController


def init():
  print("Inicio Aplicação TESTE")
  start_time = time.time()
  log = Log("TESTE")
  result = None
  
  try:
    
    database = DataBase(dictionary=True)
    controller = LeiloeirosController(database)
    
    
    result = controller.getByWordKey("paalciop")
            
  except Exception as e:
      print(f"Error: {e}")
  

  print("Resultados:",len(result or []))
  end_time = time.time()
  log.executionTime(query="fiat", api="TESTE",end=end_time, start=start_time)
  print("Aplicação Finalizada TESTE")