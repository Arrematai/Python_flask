from src.infra.database.mysql import DataBase
from src.domain.modelosAnos.repository import ModelosAnoRepository

class ModelosAnosController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = ModelosAnoRepository(self.database)
  
  def getModelosAnos(self):
    try:
      result = self.repository.findModelosAnos()
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Marcas não encontrados.")
          
  def getModelosByModeloId(self, modeloId):
    try:
      result = self.repository.findModelosByModeloId(modeloId)
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Marcas não encontrados.")