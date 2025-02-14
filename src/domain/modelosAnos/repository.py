from src.infra.database.mysql import DataBase

class ModelosAnoRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def findModelosAnos(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome FROM anos order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()

  def findModelosByModeloId(self,modeloId):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = "SELECT id, codigo, nome, modeloId, modelo FROM anosmodelos where modeloId = %s order by nome"
      self.database.socket.execute(query, (modeloId,))

      # Recuperando os resultados
      return self.database.socket.fetchall()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()
          
