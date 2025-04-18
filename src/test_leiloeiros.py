## DATABASE
from src.infra.database.mysql import DataBase

## WORDKEY
from src.domain.leiloeiros.controller import LeiloeirosController


def init():
  print("Inicio Aplicação TESTE")
  result = None
  
  try:
    
    database = DataBase(dictionary=True)
    controller = LeiloeirosController(database)
    
    # result = controller.getByWordKey("www.palaciodoleilao.com.br")
    result = controller.getByWordKey("","https://galli.app")

    print(result)

          
  except Exception as e:
      print(f"Error: {e}")
  

  # print("Resultados:",len(result or []))
  # print("Resultados:",result)
  print("Aplicação Finalizada TESTE")