from src.infra.database.mysql import DataBase

class ModelosController:

  def __init__(self, database: DataBase):
    self.database = database
  
  def getModelos(self):
      try:
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome FROM modelos order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return  self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
          
  def getModelosByMarcaId(self, marcaId: str):
    try:
      print(marcaId)
      # Executando uma consulta SELECT
      query = "SELECT id, codigo, nome FROM modelos where = %s order by nome"
      self.database.socket.execute(query, (marcaId,))

      # Recuperando os resultados
      return  self.database.socket.fetchall()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.conn.rollback()
    finally:
        self.database.close()
