from src.infra.database.mysql import DataBase
from src.domain.marcas.repository import MarcaRepository

class MarcasController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = MarcaRepository(self.database)
  
  def getMarcas(self):
    try:
      result = self.repository.findMarcas()
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Marcas não encontrados.")
  