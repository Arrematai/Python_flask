from src.infra.database.mysql import DataBase
from src.infra.service.Parallelum import ServiceParallelum
from src.helpers.seedDataBaseLocal import SeedDataBase

def init():
  print("Inicio Aplicação")
  
  database = DataBase()
  service = ServiceParallelum()
  
  seed = SeedDataBase(database=database, service=service)
  
  seed.seedModelosAnos()

  print("Aplicação Finalizada")