from src.infra.database.mysql import DataBase

class MarcaRepository:

  def __init__(self, database: DataBase):
    self.database = database
  
  def findMarcas(self):
      try:
        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome, imagem FROM marcas order by nome"
        self.database.socket.execute(query)

        # Recuperando os resultados
        return self.database.socket.fetchall()
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
          