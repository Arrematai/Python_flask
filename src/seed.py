from src.infra.database.mysql import DataBase
from src.infra.service.Parallelum import ServiceParallelum
from src.helpers.seedDataBase import SeedDataBase

def init():
  print("Inicio Aplicação")
  
  database = DataBase()
  service = ServiceParallelum()
  
  seed = SeedDataBase(database=database, service=service)
  
  seed.seedFipes()

  print("Aplicação Finalizada")