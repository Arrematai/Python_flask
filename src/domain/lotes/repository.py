from src.infra.database.mysql import DataBase

class LotesRepository:

  def __init__(self, database: DataBase):
    self.database = database
  

  def getLotesByApi(self, api: str):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM lotes where api = %s"
        self.database.socket.execute(query, (api,))

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          self.database.close()
          
  def getLotesByApiAtivos(self, api: str):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM lotes where api = %s and ativo = 1"
        self.database.socket.execute(query, (api,))

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          self.database.close()

  def getLotesByQuery(self, api: str, query: str):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      querySql = """
        SELECT * FROM lotes
        WHERE api = %s
          AND (LOWER(marca) LIKE %s OR LOWER(modelo) LIKE %s)
          AND ativo = 1
      """
      like_param = f"%{query}%"
      self.database.socket.execute(querySql, (api, like_param, like_param))

      # Recuperando os resultados
      return self.database.socket.fetchall()
          
    except Exception as e:
        self.database.close()
  
  def insertLote(self, dados):
    try:

      self.database.connection()

      campos = ", ".join(dados.keys())
      valores = ", ".join(["%s"] * len(dados))

      # Executando uma consulta SELECT
      query = f"""
        INSERT INTO lotes ({campos})
        VALUES ({valores})
      """

      # Executar com tupla de parâmetros
      self.database.socket.execute(
          query,
          list(dados.values())
      )

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()

  def updateLote(self, dados):
    try:

      self.database.connection()

      chave = "id"
      excluidos = {"id", "uuid", "created_at"}
      campos_update = {k: v for k, v in dados.items() if k not in excluidos}
      set_clause = ", ".join([f"{k} = %s" for k in campos_update])

      # Executando uma consulta SELECT
      query = f"UPDATE lotes SET {set_clause} WHERE {chave} = %s"

      # Executar com tupla de parâmetros
      self.database.socket.execute(
          query,
          list(campos_update.values()) + [dados[chave]]
      )

      # Recuperando os resultados
      self.database.conn.commit()
           
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()
