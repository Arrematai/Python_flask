from src.infra.database.mysql import DataBase

class ModelosAnosController:

  def __init__(self, database: DataBase):
    self.database = database
  
  def getModelosAnos(self):
      try:
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome FROM anos order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return  self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
          
  def getModelosByModeloId(self, modeloId):
    try:
      # Executando uma consulta SELECT
      query = "SELECT id, codigo, nome, modeloId, modelo FROM modelos where modeloId = ? order by nome"
      self.database.socket.execute(query, (modeloId,))

      # Recuperando os resultados
      return  self.database.socket.fetchall()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.conn.rollback()
    finally:
        self.database.close()
