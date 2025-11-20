from src.domain.lotes.repository import LotesRepository
from src.infra.database.mysql import DataBase
from src.infra.service.Logging import Log


class ServicePestana:
    def __init__(self, query, size, api  = None):
        self.query = query
        self.size = size
        self.api = api
        self.resultados = []
        self.log = Log("")
        self.database = DataBase(dictionary=True)
    
  
    def exec(self):
      try:
        repository = LotesRepository(self.database)

        self.resultados = repository.getLotesByQuery(self.api,self.query)

        return { "resultados": self.resultados, "http_code": 200 }
      except Exception as e:
          self.database.close()
          self.log.messageError(f"Erro resultado via banco de dados - {self.api}")
          return { "resultados": self.resultados, "http_code": 400 }