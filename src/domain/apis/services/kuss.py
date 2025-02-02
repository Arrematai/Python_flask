import os
import re
from typing import Text
from bs4 import BeautifulSoup
import requests
import uuid

from src.infra.helpers.Monta import getMonta
from src.infra.helpers.MarcaCarros import obter_marcas, replace_marcas

class ServiceKuss:
    url: Text = "https://www.claudiokussleiloes.com.br/json_edital.php"
    payload: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        self.Marcas = obter_marcas()
        self.leiloes = []
        self.resultados = []
        
    def initValue(self):
        self.data = {
            "leilaoID": "",
            "op": "P",
            "loteado": "S",
            "pag": 1,
            "pesq": {self.query}
        }
        self.headers= {
          "cookie": "PHPSESSID=4rgmf66hvajl099hji9u2m3rcg; _ga=GA1.1.2035548992.1737040179; _gcl_au=1.1.758536258.1737040179; rdtrk=%7B%22id%22%3A%2278c3e5de-d337-4ce3-bcb2-262d73dd049b%22%7D; _ga_0M0D2PNKJQ=GS1.1.1737049974.3.1.1737050020.14.0.0; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiKG5vbmUpIiwiZXh0cmFfcGFyYW1zIjp7fX0sImNyZWF0ZWRfYXQiOjE3MzcwNTAwMjAyMDZ9",
          "origin": "https://www.claudiokussleiloes.com.br",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        
    def _getLeiloesCurr(self):
      response = requests.get("https://www.claudiokussleiloes.com.br/proximos-leiloes", headers=self.headers)
      soup = BeautifulSoup(response.text, "html.parser")
      
      leiloes = soup.find_all("a", class_="btn btn-success", attrs={'target': '_self'})
      self.leiloes = [link.get('href') for link in leiloes]
      self.leiloes = [item.replace("relacao-foto/", "") for item in self.leiloes]

    def _getMarca(self, title: str):
      marca = re.split(r'/', title)
      return replace_marcas(marca[0]) if marca and marca[0] else None
    
    def _getModelo(self, title):
      modelo = re.split(r'/', title)
      return modelo[1] if modelo else None
        
    def exec (self):
      self._getLeiloesCurr()
      
      for leilao in self.leiloes:
        self.data["leilaoID"] = leilao
        response = requests.post(self.url, headers=self.headers, data=self.data)
        
        if response.status_code != 200:
            print(f"Erro ao acessar o site na página: {response.status_code}")
            continue
          
        data = response.json()
        
        
        if len(data) <= 0:
          continue
                
        for item in data:
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": item["lote"],
                "chassi": None,
                "valor_fipe": None,
                "valor_atual": item["valor"],
                "tipo_veiculo": None,
                "marca": self._getMarca(item["bem"]),
                "modelo": self._getModelo(item["bem"]),
                "monta": getMonta(""),
                "ano": item["ano"],
                "thumb": item["foto"],
                "link": f"https://www.claudiokussleiloes.com.br/lance/{leilao}/{item["lote"]}",
                "leiloeiro":"Claudio Kuss",
                "ativo": 1,
            }
            # Adiciona o dicionário à lista de resultados
            self.resultados.append(resultado)

        # Exibe os resultados
        # print(self.resultados[0])
        return self.resultados
