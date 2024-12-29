import time
import requests
from src.infra.database.mysql import DataBase
from src.infra.service.Parallelum import ServiceParallelum

class SeedDataBase:
    def __init__(self, database: DataBase, service: ServiceParallelum):
      self.database = database
      self.service = service
      
      
    def seedMarcas(self):
      marcas = self.service.getMarcas()
      
      query = """
      INSERT INTO marcas (codigo, nome)
      VALUES (%s, %s)
      ON DUPLICATE KEY UPDATE
      codigo = VALUES(codigo),
      nome = VALUES(nome);
      """
      
      if not marcas or len(marcas) <= 0:
        print("API nao retornou marcas")
        return 
      
      try:
        data = [(item['codigo'], item['nome']) for item in marcas]
        # Insert multiple rows
        self.database.socket.executemany(query,data)
        
        # Commit changes
        self.database.conn.commit()
        print(f"{self.database.socket.rowcount} linhas inseridas com sucesso.")
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()

      
    def seedModelos(self):
      try:
        # Executando uma consulta SELECT
        query = "SELECT id, codigo, nome FROM marcas"
        self.database.socket.execute(query)

        # Recuperando os resultados
        marcas = self.database.socket.fetchall()
        
        
        try:
          max_tentativas = 3
          tentativa = 0
          
          while tentativa < max_tentativas:
            tentativa += 1
          
          for marca in marcas:
            print(">>>> MARCA", marca)
            modelos = self.service.getModelos(marca[1])
            
            print(modelos)
            
            query = """
            INSERT INTO modelos (codigo, nome, marcaId, marca)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            codigo = VALUES(codigo),
            nome = VALUES(nome);
            """
            
            data = [(item['codigo'], item['nome'], marca[0], marca[2]) for item in modelos]
            # Insert multiple rows
            self.database.socket.executemany(query,data)
            # Commit changes
            self.database.conn.commit()
            print(f"{self.database.socket.rowcount} linhas inseridas com sucesso.")
            print("____________________________________________________________")
            print("")
            time.sleep(10)
        except requests.exceptions.RequestException as e:
          print(f"Erro: {e}. Retentando...")
          
        time.sleep(20)
          
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()
          
    def seedModelosAnos(self):
      try:
        lastID = 6223
        subQuery = """
            SELECT 
                modelos.id, 
                modelos.codigo, 
                modelos.nome, 
                marcas.codigo AS codigoMarca, 
                marcas.nome 
            FROM 
                modelos 
            LEFT JOIN 
                marcas 
            ON 
                marcas.id = modelos.marcaId
            """
        
        # Executando uma consulta SELECT
        if lastID:
          query = subQuery + " " +"""
            WHERE 
                modelos.id < %s 
            ORDER BY 
                modelos.id DESC;
            """
          args = (lastID,) ## tem q ser uma tupla
          self.database.socket.execute(query,args) 
        else:
          query = subQuery + " " + """
            ORDER BY 
                modelos.id DESC;
            """
          self.database.socket.execute(query)
        

        # Recuperando os resultados
        modelos = self.database.socket.fetchall()
        
        
        try:
          max_tentativas = 3
          tentativa = 0
          
          while tentativa < max_tentativas:
            tentativa += 1
          
          for modelo in modelos:
            print(">>>> MODELO", modelo)
            dados = self.service.getAnos(modelo[3],modelo[1])
            
            query = """
              INSERT INTO anos (codigo, nome, modeloId, modelo)
              VALUES (%s, %s, %s, %s)
            """
            
            
            data = []
            
            for d in dados:
              select = "SELECT count(id) as count FROM arrematai.anos where modelo = %s and codigo = %s and nome = %s limit 1;"
              self.database.socket.execute(select, (modelo[2], d['codigo'], d['nome']))
              resultados = self.database.socket.fetchone()
              if resultados[0] == 0:
                data.append((d['codigo'], d['nome'], modelo[0], modelo[2]))

            print(data)
            # Insert multiple rows
            self.database.socket.executemany(query,data)
            # Commit changes
            self.database.conn.commit()
            print(f"{self.database.socket.rowcount} linhas inseridas com sucesso.")
            print("____________________________________________________________")
            print("")
        except requests.exceptions.RequestException as e:
          print(f"Erro: {e}. Retentando...")
          
        time.sleep(20)
          
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()

    def seedFipes(self):
      try:
        lastID = None
        subQuery = """
            SELECT anos.id, anos.codigo, anos.nome, modeloId, modelo, marcaId, marca FROM anos LEFT JOIN modelos ON modelos.id = modeloId
            """
        
        # Executando uma consulta SELECT
        if lastID:
          query = subQuery + " " +"""
            WHERE 
                anos.id < %s 
            ORDER BY 
                anos.id DESC;
            """
          args = (lastID,) ## tem q ser uma tupla
          self.database.socket.execute(query,args) 
        else:
          query = subQuery + " " + """
            ORDER BY 
                anos.id DESC;
            """
          self.database.socket.execute(query)
        

        # Recuperando os resultados
        modelosAnos = self.database.socket.fetchall()
        
        try:
          max_tentativas = 3
          tentativa = 0
          
          while tentativa < max_tentativas:
            tentativa += 1
          
          for modelo in modelosAnos:
            print(">>>> MODEL0", modelo)
            dados = self.service.getFipe(modelo[5],modelo[3],modelo[1])
  
            print(dados)
            
            if not dados:
              continue
            
            # Insert multiple rows
            query = """
              INSERT INTO anos (AnoModelo, CodigoFipe, Combustivel, Marca, MesReferencia, Modelo, SiglaCombustivel, TipoVeiculo, Valor, modeloId, marcaId)
              VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)
              ON DUPLICATE KEY UPDATE
              CodigoFipe = VALUES(CodigoFipe),
            """
            self.database.socket.executemany(query,dados + modelo[5] + modelo[3])
            # Commit changes
            self.database.conn.commit()
            print(f"{self.database.socket.rowcount} linhas inseridas com sucesso.")
            print("____________________________________________________________")
            print("")
        except requests.exceptions.RequestException as e:
          print(f"Erro: {e}. Retentando...")
          
        time.sleep(20)
          
      except Exception as e:
          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          self.database.close()