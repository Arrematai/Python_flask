from src.infra.database.mysql import DataBase

class ModelosRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def findModelos(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome FROM modelos order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()

  def findModelosByMarcaId(self,marcaId):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = "SELECT id, codigo, nome FROM modelos where marcaId = %s order by nome"
      self.database.socket.execute(query, (marcaId,))

      # Recuperando os resultados
      return self.database.socket.fetchall()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()
          
        