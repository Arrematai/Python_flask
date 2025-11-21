import uuid
from src.infra.database.mysql import DataBase

class RastreioRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def findRastreioByCodigo(self, codigo: str):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT dados FROM rastreamento_veiculos WHERE codigo = %s LIMIT 1"
        self.database.socket.execute(query, (codigo,))

        # Recuperando os resultados
        return self.database.socket.fetchone()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
          
  def insert(self, dados):
    try:
      
      codigo = str(uuid.uuid4())

      print(dados)
      self.database.connection()
      # Executando uma consulta SELECT
      query = """
      INSERT INTO `rastreamento_veiculos` 
      (`codigo`, `ip`, `url_destino`,`dados`) 
      VALUES (%s, %s, %s, %s)
      """

      # Executar com tupla de parâmetros
      self.database.socket.execute(
          query,
          (
              codigo,
              dados["ip"],
              dados["url_destino"],
              dados["dados"],
          )
      )

      # Recuperando os resultados
      self.database.conn.commit()
      
      return {
          "codigo": codigo,
          "ip": dados["ip"],
          "url_destino": dados["url_destino"],
          "dados": dados["dados"]
      }
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()