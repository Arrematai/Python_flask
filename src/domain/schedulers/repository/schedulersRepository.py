from src.infra.database.mysql import DataBase

class SchedulersRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def getSchedulers(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = f"SELECT * FROM schedulers where ativo = 1"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
