from src.infra.database.mysql import DataBase

class SchedulersLogRepository:

  def __init__(self, database: DataBase):
    self.database = database
  

  def insertLog(self, dados):
    try:

      print(dados)
      self.database.connection()
      # Executando uma consulta SELECT
      query = """
      INSERT INTO `log_schedulers` 
      (`nome`,`duration`, `results`, `status`) 
      VALUES (%s, %s, %s, %s)
      """

      # Executar com tupla de parâmetros
      self.database.socket.execute(
          query,
          (
              dados["nome"],
              dados["duration"],
              dados["results"],
              dados["status"],
          )
      )

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()