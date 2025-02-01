from src.infra.database.mysql import DataBase

class ApisRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def getApis(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM apis where ativo = 1 and status_site = 1"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
          
  def getApi(self, nome: str):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM apis where nome = %s and ativo = 1 and status_site = 1"
        self.database.socket.execute(query, (nome,))

        # Recuperando os resultados
        return self.database.socket.fetchone()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
          