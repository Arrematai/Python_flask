import time
import requests
from src.infra.database.mysql import DataBase
from src.infra.service.Parallelum import ServiceParallelum


def readLastId():
  with open('lastId.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()
  print(conteudo)
  return conteudo

def writeLastId(conteudo):
  if(conteudo):
    with open('lastId.txt', 'w', encoding='utf-8') as arquivo:
      arquivo.write(f'{conteudo}')




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
        lastID = 2052
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
                modelos.id <= %s 
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
              INSERT INTO AnosModelos (codigo, nome, modeloId, modelo)
              VALUES (%s, %s, %s, %s)
            """
            
            
            data = []
            
            for d in dados:
              select = "SELECT count(id) as count FROM AnosModelos where modelo = %s and codigo = %s and nome = %s limit 1;"
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
        readLastId()
        lastID = readLastId()
        ultimo = None
        subQuery = """
            SELECT anosmodelos.id, anosmodelos.codigo, anosmodelos.nome, modelos.codigo, modelo, modelos.id, marcas.codigo, marca, marcas.id 
            FROM anosmodelos 
            LEFT JOIN modelos ON modelos.id = modeloId
            LEFT JOIN marcas ON marcas.id = marcaId
            """
        
        # Executando uma consulta SELECT
        if lastID:
          query = subQuery + " " +"""
            WHERE 
                anosmodelos.id >= %s 
            ORDER BY 
                anosmodelos.id ASC;
            """
          args = (lastID,) ## tem q ser uma tupla
          self.database.socket.execute(query,args) 
        else:
          query = subQuery + " " + """
            ORDER BY 
                anosmodelos.id ASC;
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
              ultimo = modelo[0]
              print(">>>> ANOMODELO", modelo)
              dados = self.service.getFipe(modelo[6],modelo[3],modelo[1])
    
              if not dados:
                continue
              else:
                dados = dados["AnoModelo"],dados["CodigoFipe"],dados["Combustivel"],dados["Marca"],dados["MesReferencia"],dados["Modelo"],dados["SiglaCombustivel"],dados["TipoVeiculo"],dados["Valor"],modelo[5],modelo[8]
              
              print("Dados", dados)
              
              # check exist 
              select = "SELECT id FROM fipes WHERE AnoModelo = %s and modeloId = %s and marcaId = %s limit 1;"
              self.database.socket.execute(select, (dados[0], dados[9], dados[10]))
              resultados = self.database.socket.fetchone()
              
              print("Resultados", resultados)
                
              if not resultados:
                # Insert row
                query = """
                  INSERT INTO fipes (AnoModelo, CodigoFipe, Combustivel, Marca, MesReferencia, Modelo, SiglaCombustivel, TipoVeiculo, Valor, modeloId, marcaId)
                  VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)
                """
                
                self.database.socket.execute(query,dados)
                print(f"{self.database.socket.rowcount} linha inserida com sucesso.")
              else:
                # update row
                query = """
                UPDATE fipes
                SET 
                    AnoModelo = %s,
                    CodigoFipe = %s,
                    Combustivel = %s,
                    Marca = %s,
                    MesReferencia = %s,
                    Modelo = %s,
                    SiglaCombustivel = %s,
                    TipoVeiculo = %s,
                    Valor = %s,
                    modeloId = %s,
                    marcaId = %s
                WHERE id = %s;
                """
                self.database.socket.execute(query,dados + (resultados[0],))
                print(f"{self.database.socket.rowcount} linha atualizada com sucesso.")
                
              # Commit changes
              self.database.conn.commit()
              print("____________________________________________________________")
              print("")
        except requests.exceptions.RequestException as e:
          print(f"Erro: {e}. Retentando...")
          
        time.sleep(20)
          
      except Exception as e:

          print(f"Error: {e}")
          self.database.conn.rollback()
      finally:
          writeLastId(ultimo)
          self.database.close()