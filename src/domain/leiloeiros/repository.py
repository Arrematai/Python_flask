from src.infra.database.mysql import DataBase

class LeiloeirosRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def findLeiloeiros(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM leiloeiros order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
          
  def findLeiloeirosStatusSite(self, status = None):
    try:
      query = ""
      self.database.connection()

      if status:
        query = "SELECT * FROM leiloeiros where status_site = %s group by site order by site"
        self.database.socket.execute(query, (status,))
      else:
        query = "SELECT * FROM leiloeiros group by site order by site"
        self.database.socket.execute(query)
        

      # Recuperando os resultados
      return self.database.socket.fetchall()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()
          
  def findLeiloeirosUniqueSite(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM leiloeiros group by site order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
          
  def filterByEstado(self, estado):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT * FROM leiloeiros where estado = %s order by nome"
        self.database.socket.execute(query, (estado,))

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
          
  def filterEstados(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT estado FROM leiloeiros group by estado order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
          
  def getLeiloeirosByWordKey(self, wordKey):
    try:
      self.database.connection()
      # Executando uma consulta SELECT
      query = """
        SELECT *
        FROM leiloeiros 
        WHERE nome LIKE %s 
          OR site LIKE %s 
          OR email LIKE %s
        group by id
        """
      valor = (f"%{wordKey}%")
      valores = (valor,valor,valor)
      self.database.socket.execute(query, valores)

      # Recuperando os resultados
      return self.database.socket.fetchall()
          
    except Exception as e:
        print(f"Error: {e}")
        self.database.close()
        
  def updateStatusSite(self, id, status):
    try:
      self.database.connection()
      
      query = """ UPDATE leiloeiros 
      SET  status_site = %s, updated_at = NOW()
      WHERE id = %s """
      
      
      valores = (status, id)
      
      self.database.socket.execute(query, valores)
      self.database.conn.commit()
      
    except Exception as e:
        print(f"Error: {e}")
        self.database.conn.rollback()