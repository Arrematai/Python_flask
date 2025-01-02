from src.infra.database.mysql import DataBase

class FipesController:

  def __init__(self, database: DataBase):
    self.database = database
  
  def getCarro(self, marcaId, modeloId, AnoModelo):
      try:
        # Executando uma consulta SELECT
        query = "SELECT id, AnoModelo, CodigoFipe, Combustivel, Marca, marcaId, MesReferencia, Modelo, modeloId, SiglaCombustivel, TipoVeiculo, Valor FROM anos where AnoModelo = ? and marcaId = ? and modeloId = ? order by AnoModelo"
        self.database.socket.execute(query, (marcaId, modeloId, AnoModelo))

        # Recuperando os resultados
        return  self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
          
