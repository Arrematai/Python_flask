import os
# import logging
from typing import Text
import requests
import uuid
from requests.exceptions import HTTPError

from src.helpers.Monta import getMonta


class ServicePestana:
    url: Text = 'https://www.pestanaleiloes.com.br/api/v2/lote'
    payload: Text
    headers: Text
    resultados: list = []

    def __init__(self, query: str, size: int):
        self.query = query
        self.size = size
        self.resultados = []
        self.initValue()
        
    def initValue(self):
        self.headers= {
          # "Content-Type": "application/json"
            # "cookie": "SERVERUSED=c2364dd7264f0ff2; _gcl_au=1.1.578135360.1736975390; _gid=GA1.3.93877518.1736975391; AdoptVisitorId=BwTgpsDGIIYOwFoAMICMwEBYDMwwICMRMYEAmAgMwFY4ZKwzJLUg; rdtrk=%7B%22id%22%3A%22e2bf9a58-2aaf-48c6-9dbc-79283b9aff4f%22%7D; leiloes_logged=false; _hjSessionUser_5174377=eyJpZCI6IjRiNzJiMTkxLTQ2ZTQtNTNiMi1iZDM1LTVhNmFjYWZmZGYyNyIsImNyZWF0ZWQiOjE3MzY5NzUzODg2MjYsImV4aXN0aW5nIjp0cnVlfQ==; _clck=ce3bcj%7C2%7Cfsm%7C0%7C1841; _hjSession_5174377=eyJpZCI6IjkzM2QwYjhhLWQwMTEtNDhhZi1hODk4LTI4OGI5ZDcwYTRmMSIsImMiOjE3MzcwNjkwMjg3NDUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiKG5vbmUpIiwiZXh0cmFfcGFyYW1zIjp7fX0sImNyZWF0ZWRfYXQiOjE3MzcwNjkwMjk2NDl9; AdoptConsent=N4Ig7gpgRgzglgFwgSQCIgFwgEwA4CGUADAMwBsA7ALQQUVlUAs+2RVUUJAZlQJyO4SvfEVxQAxgBNcIADQgAbnHgIA9gCdkkzCFy8IuccOpFeARlxMSuCO374q2KFwCsFfFwjZxXM3JCqAA4IyAB2ACr4AOYwmADaIBAAorhkaAAKqKgAmv4ASriBqLx5oaos/tkAFlW8AHJkzAC2ZPniFADqAPqhcLhmUP4AHgBS2OlQqgCuAGoAEgBi/lFVXAA2UB3jocggALryQQgA8lMIkTHxByDiqqEwEKEh2ljIUOFcAIJT/hAKj+cAJ6BCA6BB5ADSAEUKJJof5bvcATMIOp4HdMER5FNApJ8EhJJ8EDpWNgXFQiGYqGYyOFsCQMGYiBgSEQAHRM3gALRAAF8gA=; _uetsid=0f276cc0d38511efbd2839ae1b2ffba1; _uetvid=0f27ba30d38511efa66611aa1f8ab2a9; _ga=GA1.3.649137075.1736975391; _gat_UA-25815487-1=1; _gat_gtag_UA_25815487_1=1; _clsk=1k00q1u%7C1737069222415%7C4%7C1%7Ch.clarity.ms%2Fcollect; _ga_DH14FS8PNZ=GS1.1.1737069034.5.1.1737069237.37.0.0; _ga_DCZGFQBFF2=GS1.1.1737069036.3.1.1737069237.43.0.0",
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            # "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            # "Connection": "keep-alive",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
            # "if-none-match": 'W/"64e-drvVFgOkuE0pw5rY/LcfM3heDVM"',
            # "referer": "https://www.pestanaleiloes.com.br/",
            # "sec-ch-ua-platform": "Windows",
            # "sec-fetch-dest": "empty",
            # "sec-fetch-mode": "cors",
            # "sec-fetch-site": "same-origin",
        }
        
    def exec (self):
        try:
          response = requests.get(self.url, headers=self.headers)
          response.raise_for_status()
        except HTTPError as http_err:
          print(f"HTTP error occurred: {http_err}") 
        
        if response.status_code != 200:
          print(f"Erro ao acessar o site na página: {response.status_code}")
          return []
          
        data = response.json()
        
        
        automoveis = list(filter(lambda item: item["bens"][0]["tipoBem"]["id"] == 421, data))
        
        
        if automoveis and len(automoveis) > 0:
          for automovel in automoveis:
            
            # Marca
            marca = next(filter(lambda item: item["tipo"] == 1733520656132, automovel["bens"][0]["caracteristicas"]), "Não Informado")
            marca = marca["valor"] if "valor" in marca else None
            # Modelo
            carro = next(filter(lambda item: item["tipo"] == 1733520657548, automovel["bens"][0]["caracteristicas"]), "")
            versao = next(filter(lambda item: item["tipo"] == 1733520660276, automovel["bens"][0]["caracteristicas"]), "")
            combustivel = next(filter(lambda item: item["tipo"] == 1733520672455, automovel["bens"][0]["caracteristicas"]), "")
            
            carro = carro["valor"] if "valor" in carro else None
            versao = versao["valor"] if "valor" in versao else None
            combustivel = combustivel["valor"] if "valor" in combustivel else None
            
            modelo = f"{carro} {versao} {combustivel}"
            
            # query enviada não é igual ao modelo e marca
            if (marca.lower() != self.query.lower()) and (self.query.lower() not in modelo.lower()):
              continue
            
            
            monta = next(filter(lambda item: item["tipo"] == 1733520634927, automovel["bens"][0]["caracteristicas"]), "Não Informado")
            ano_inicial = next(filter(lambda item: item["tipo"] == 12345, automovel["bens"][0]["caracteristicas"]), "")
            ano_final = next(filter(lambda item: item["tipo"] == 1733520664332, automovel["bens"][0]["caracteristicas"]), "")
            thumb = automovel["bens"][0]["imagens"][0]["original"]
            
            
            ano_inicial = ano_inicial["valor"] if "valor" in ano_inicial else None
            ano_final = ano_final["valor"] if "valor" in ano_final else None
            
            ano = f"{ano_inicial}/{ano_final}" if ano_inicial and ano_final else f"{ano_inicial}" if ano_inicial else f"{ano_final}" if ano_final else ""
            monta = monta["valor"] if "valor" in monta else None
            lote = automovel["id"]
            leilao = automovel["leilao"]
            valor_atual = automovel["valorInicial"]
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote":  lote,
                "chassi": "",
                "valor_fipe": None,
                "valor_atual": valor_atual,
                "tipo_veiculo": "",
                "marca": marca,
                "modelo": modelo,
                "monta": getMonta(monta),
                "ano": ano,
                "thumb": f"https://ged.pestanaleiloes.com.br/ged/{thumb}",
                "link": f"https://www.pestanaleiloes.com.br/agenda-de-leiloes/{leilao}/{lote}",
                "leiloeiro":"Pestana Leilões",
                "ativo": 1,
            }
            
            self.resultados.append(resultado)

        # Exibe os resultados
        print(len(self.resultados))
        # return jsonify(resultados)
        return self.resultados
