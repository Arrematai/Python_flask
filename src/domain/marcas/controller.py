from src.infra.database.mysql import DataBase

class MarcasController:

  def __init__(self, database: DataBase):
    self.database = database
  
  def getMarcas(self):
      try:
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome FROM marcas order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
  