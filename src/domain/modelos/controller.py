from src.infra.database.mysql import DataBase
from src.domain.modelos.repository import  ModelosRepository


class ModelosController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = ModelosRepository(self.database)
  
  def getModelos(self):
    try:
      result = self.repository.findModelos()
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Marcas não encontrados.")
          
  def getModelosByMarcaId(self, marcaId: str):
    try:
      result = self.repository.findModelosByMarcaId(marcaId)
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Marcas não encontrados.")
