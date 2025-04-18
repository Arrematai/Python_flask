import uuid
from src.infra.database.mysql import DataBase

class LogsRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def insertApis(self, dados):
    try:

      print(dados)
      self.database.connection()
      # Executando uma consulta SELECT
      query = """
      INSERT INTO `log_apis` 
      (`uuid`, `ip`, `api`,`query`, `http_code`, `duration`, `results`) 
      VALUES (%s, %s, %s, %s, %s, %s, %s)
      """

      # Executar com tupla de parâmetros
      self.database.socket.execute(
          query,
          (
              str(uuid.uuid4()),
              dados["ip"],
              dados["api"],
              dados["query"],
              dados["http_code"],
              dados["duration"],
              dados["results"],
          )
      )

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()


  def insertLeiloeiros(self, dados):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = "INSERT INTO `log_leiloeiros` " \
      "(`uuid`, `ip`, `palavra`, `tipo`, `duration`, `results`) " \
      "VALUES %s, %s, %s, %s,%s, %i)"

      self.database.socket.execute(query, 
                                   (str(uuid.uuid4()), dados["ip"]), dados["palavra"], dados["tipo"],dados["duration"], dados["results"])

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()


  def insertCalc(self, dados):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = "INSERT INTO `log_leiloeiros` " \
      "(`uuid`, `ip`, `uso`, `fipe`, `monta`, `comissao`, `despesa`, `disponivel`, `lance_max`,`venda`,`lucro`) " \
      "VALUES %s, %s, %s, %i,%i, %i,%i,%i,%i,%i,%i)"

      self.database.socket.execute(query, 
                                   (str(uuid.uuid4()), dados["ip"]), dados["uso"], dados["fipe"],dados["monta"], dados["comissao"], dados["despesa"], dados["disponivel"],dados['lance_max'],dados["venda"],dados["lucro"])

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()


# INSERT INTO `arrematai`.`response_apis` (`uuid`, `ip`, `api`, `method`, `http_code`, `duration`, `results`, `url`) VALUES ('fwerfnwefwe', 'fwef', 'fwefw', 'fwefw', 'fwefw', 'fwefwe', '8', 'fwefwefw');
