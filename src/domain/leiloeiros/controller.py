
import re
from urllib.parse import urlparse
import time


from src.infra.database.mysql import DataBase
from src.domain.leiloeiros.repository import LeiloeirosRepository
from src.domain.log.repository import LogsRepository
from src.domain.leiloeiros.useCaseWordKey import UseCaseWordKey

class LeiloeirosController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = LeiloeirosRepository(self.database)
    self.repositoryLog = LogsRepository(self.database)
  
  def getLeiloeiros(self):  
      try:
        result = self.repository.findLeiloeiros()
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise Exception("Leiloeiros não encontrados.")

  def getLeiloeirosWithLogo(self):  
    try:
      result = self.repository.findLeiloeirosWithLogo()
      
      return result
          
    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Leiloeiros não encontrados.")
        
  def getLeiloeirosByEstado(self, estado):
      try:
        result = self.repository.filterByEstado(estado)
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise Exception("Leiloeiros por estado não encontrados.")
        
  def getEstados(self):
      try:
        result = self.repository.filterEstados()
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise Exception("Estados não encontrados.")
        
        
  def getByWordKey(self, ip, wordKey: str):
    try:
      resultados = []
      start_time = time.time()
      if self.is_url(wordKey) or "www" in wordKey:
        wordKey = self.clean_url(wordKey).replace(".", " ").replace("-"," ")
      if '.' in wordKey:
        wordKey = wordKey.split('.')
        wordKey = wordKey[0]

      print(wordKey)

      print("Palavra Chave", wordKey)
      newListLeiloeiros = self.repository.getLeiloeirosByWordKey(wordKey)
      
      
      ## BANCO DE DADOS
      if newListLeiloeiros and len(newListLeiloeiros) > 0:
        resultados = {
           "tipo": 'banco',
           'leiloeiros': newListLeiloeiros,
        }
      else:
        listLeiloeiros = self.getLeiloeiros()
        resultados = UseCaseWordKey(wordKey, listLeiloeiros)
    
      end_time = time.time()
      self.repositoryLog.insertLeiloeiros({
         "ip": ip,
         "palavra": wordKey,
         'tipo': resultados["tipo"],
         "duration": end_time - start_time,
         "results": len(resultados["leiloeiros"])
      })
      return resultados
    except Exception as e:
      print("ERROR:",e)
      raise Exception("Nem um leiloeiro encontrado na busca.")
    
  def is_url(self, url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)
  
  def clean_url(self, url):
    # Parseia a URL para extrair o domínio
    parsed_url = urlparse(url)
    
    # Pega o netloc (domínio) ou, se não existir, usa a URL inteira
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path

    # Remove www. do início
    domain = re.sub(r"^www\.", "", domain)

    # Remove tudo depois do primeiro domínio de nível superior (TLD)
    domain = re.sub(r"\..*$", "", domain)

    print('aqui',domain)

    # Remove qualquer barra final
    return domain.strip("/")
  
