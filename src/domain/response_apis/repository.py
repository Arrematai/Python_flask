import uuid
from src.infra.database.mysql import DataBase

class ResponseApisRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def insert(self, dados):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = "INSERT INTO `response_apis` " \
      "(`uuid`, `ip`, `api`, `method`, `http_code`, `duration`, `results`, `url`) " \
      "VALUES %s, %s, %s, %s,%s, %s,%i,%s)"

      self.database.socket.execute(query, 
                                   (str(uuid.uuid4()), dados["ip"]), dados["api"], dados["method"],dados["http_code"], dados["duration"], dados["results"], dados["url"])

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()


# INSERT INTO `arrematai`.`response_apis` (`uuid`, `ip`, `api`, `method`, `http_code`, `duration`, `results`, `url`) VALUES ('fwerfnwefwe', 'fwef', 'fwefw', 'fwefw', 'fwefw', 'fwefwe', '8', 'fwefwefw');
