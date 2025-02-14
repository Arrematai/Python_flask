from src.infra.database.mysql import DataBase
from src.domain.fipes.repository import FipesRepository

class FipesController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = FipesRepository(self.database)
  
  def getCarro(self, marcaId, modeloId, AnoModelo):
    try:
      result = self.repository.findCarro(marcaId, modeloId, AnoModelo)
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Carro não encontrados.")
