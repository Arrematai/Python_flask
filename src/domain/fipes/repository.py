from src.infra.database.mysql import DataBase

class FipesRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def findCarro(self,marcaId, modeloId, AnoModelo):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = "SELECT id, AnoModelo, CodigoFipe, Combustivel, Marca, marcaId, MesReferencia, Modelo, modeloId, SiglaCombustivel, TipoVeiculo, Valor FROM fipes where marcaId = %s and modeloId = %s and AnoModelo = %s order by AnoModelo LIMIT 1"
      self.database.socket.execute(query, (marcaId, modeloId, AnoModelo))

      # Recuperando os resultados
      return self.database.socket.fetchone()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()

