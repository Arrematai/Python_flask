
import re
from urllib.parse import urlparse
import time


from src.infra.database.mysql import DataBase
from src.domain.rastreio.repository import RastreioRepository
from src.domain.log.repository import LogsRepository

class RastreioController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = RastreioRepository(self.database)
    self.repositoryLog = LogsRepository(self.database)
  
  def getRastreioByCodigo(self, codigo: str):  
      try:
        if not codigo:
          raise Exception("Deve enviar codigo.") 
        
        result = self.repository.findRastreioByCodigo(codigo)
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise Exception("Rastreio não encontrado.")
        
  def insert(self, ip: str , url_destino: str, dados: str):  
      try:
        result = self.repository.insert({ "ip": ip, "url_destino": url_destino, "dados": dados })
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise Exception("Rastreio não encontrado.")

  
