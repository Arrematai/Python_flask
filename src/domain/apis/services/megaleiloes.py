import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup
import json
import urllib3
import uuid

from src.infra.helpers.MarcaCarros import obter_marcas, match_marca
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log


# Desativando avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ServiceMega:
    url: Text = "https://1a8o5m7x6q-dsn.algolia.net/1/indexes/Items/query?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser&x-algolia-application-id=1A8O5M7X6Q&x-algolia-api-key=055311365c6f5cdd0d1bff3e0acba7ae"
    payload: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.resultados = []
        self.Marcas = obter_marcas()
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.data = {"params":f"query={self.query}&page=0&hitsPerPage={self.size}"}
        
        self.headers= {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.megaleiloes.com.br",
        "referer": "https://www.megaleiloes.com.br/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
        
    def _getModelo(self,title, marca):
      
      # padrao = r"\b(?:Carro\s+)?Fiat\s+([A-Za-z0-9\s]+)(?:\s*-\s*(\d{4}(?:/\d{4})?))?\b"
      padrao = r"\b(\w+)\s+(\w+(\s+\w+)*)(?:\s*-\s*(\d{4}(?:/\d{4})?))?\b"
      match = re.search(padrao, title)
      return re.sub(rf'{marca}', '', match.group(2).strip(), flags=re.IGNORECASE) if match and match.group(2) else None
      
      
    def _getAno(self, title):
        ano_match = re.search(r'\b(\d{4})\b', title)
        return ano_match.group(1) if ano_match else None

      
    def _getMarca(self,title):
      existeMarca = next((m for m in self.Marcas if m["nome"].lower() in title.lower()), None)
      
      if existeMarca:
        return existeMarca["nome"]
      else:
          match = match_marca(title)
          return match

    
        
    def exec(self):
      response = requests.post(self.url, json=self.data, headers=self.headers)
      
      
      if response.status_code != 200:
          self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
          return { "resultados": self.resultados, "http_code": response.status_code }
      
      data = response.json()
      
      if not data: 
        return []
      
      ## filtra categoria carro "category": "Veículos"
      carros = list(filter(lambda x: x['category'] == "Veículos", data.get("hits")))
      
      
      ## filtra batch_status 0(Em breve) e 1(Aberto para lances)
      carros = list(filter(lambda x: x["batch_status"] == 0 or x['batch_status'] == 1, carros))
              
    
      for carro in carros:
        title = carro["headline"]
        valor_inicial = carro["first_instance_value"]
        link = carro["url"]
        thumb = carro["image_path"]
        lote = carro["batch_id"]
        marca = self._getMarca(title)
        modelo = self._getModelo(title, marca)
        ano = self._getAno(title)
        
      
        resultado = {
              "uuid": str(uuid.uuid4()),
              "lote": lote,
              "chassi": None,
              "valor_fipe": None,
              "valor_atual":  valor_inicial,
              "tipo_veiculo": None,
              "marca": marca,
              "modelo": modelo,
              "monta": getMonta(""),
              "ano": ano,
              "thumb": thumb,
              "link": link,
              "leiloeiro":"Mega Leilões",
              "ativo": 1,
          }
          
        #Adiciona o dicionário à lista de resultados
        self.resultados.append(resultado)


      return { "resultados": self.resultados, "http_code": response.status_code }

