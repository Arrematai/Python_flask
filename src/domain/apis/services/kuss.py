import os
# import logging
from typing import Text
from bs4 import BeautifulSoup
import requests
import uuid


##!! SEM UMA FORMA DE PEGAR OS DADOS DE FORMA ACEITAVEL

class ServiceKuss:
    url: Text = "https://api.scraperapi.com/"
    payload: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        self.leiloes = []
        self.resultados = []
        
    def initValue(self):
        self.data = {
            "leilaoID": "",
            "op": "P",
            "loteado": "N",
            "pag": 1,
            "pesq": {self.query}
        }
        self.params = {
          'api_key': '840949ffec9109750f05ac7fc9fdf4b4',
          'url': f'https://www.claudiokussleiloes.com.br/json_edital.php',
          'country_code': 'us',
          'device_type': 'desktop'
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

        
    def exec (self):
      self._getLeiloesCurr()
      
      for leilao in self.leiloes:
        self.params["leilaoID"] = leilao
        response = requests.post(self.url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"Erro ao acessar o site na página: {response.status_code}")
            return []
          
        data = response.json()
        print(data)
        
        
        
        # resultados = []
        # for item in data.get('data', {}).get('results', {}).get('content', []):
        #     resultado = {
        #         "uuid": str(uuid.uuid4()),
        #         "lote": item.get("lotNumberStr"),
        #         "chassi": item.get("fv"),
        #         "valor_fipe": item.get("la"),
        #         "valor_atual": item.get("hb"),
        #         "tipo_veiculo": item.get("vehicleType"),
        #         "marca": item.get("mkn"),
        #         "modelo": item.get("lm"),
        #         "monta": item.get("damageClassification"),
        #         "ano": item.get("manufactureYear"),
        #         "thumb": item.get("tims").replace("thumbnail","vga"),
        #         "link": "https://www.copart.com.br/lot/" + str(item.get("lotNumberStr")),
        #         "leiloeiro":"COPART",
        #         "ativo": 1,
        #     }
        #     # Adiciona o dicionário à lista de resultados
        #     resultados.append(resultado)

        # Exibe os resultados
        # print(len(resultados))
        # return jsonify(resultados)
        # return resultados
