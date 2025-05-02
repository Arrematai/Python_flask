from typing import Text


from src.infra.database.mysql import DataBase
from src.domain.lotes.repository import LotesRepository
from src.infra.service.Logging import Log

class ServiceReceitaFederal:

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.resultados = []
        self.log = Log("")
        self.database = DataBase(dictionary=True)
    
  
    def exec(self):
      try:
        repository = LotesRepository(self.database)

        self.resultados = repository.getLotesByQuery("receitafederal",self.query)

        return { "resultados": self.resultados, "http_code": 200 }
      except Exception as e:
          self.database.close()
          self.log.messageError(f"Erro resultado via banco de dados")
          return { "resultados": self.resultados, "http_code": 400 }
