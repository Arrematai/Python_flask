import json
import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup



class ServiceMgl:
    url: Text = "https://www.mgl.com.br/ApiFeatures/GetBusca/1/1/0?"
    parametros: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        
    def initValue(self):
        self.payload = {
                "RangeValores": 0,
                "Scopo": 0,
                "IgnoreScopo": 0,
                "OrientacaoBusca": 0,
                "Mapa": "",
                "Busca": "fiat",
                "ID_Categoria": 0,
                "ID_Estado": 0,
                "ID_Cidade": 0,
                "Bairro": "",
                "ID_Regiao": 0,
                "ValorMinSelecionado": 0,
                "ValorMaxSelecionado": 0,
                "CFGs": "[]",
                "Pagina": 1,
                "sInL": "",
                "Ordem": 0,
                "QtdPorPagina": 24,
                "SubStatus": [],
                "ID_Leiloes_Status": [],
                "PaginaIndex": 1,
                "BuscaProcesso": "",
                "NomesPartes": "",
                "CodLeilao": "",
                "TiposLeiloes": [],
                "PracaAtual": 0,
                "DataAbertura": "",
                "DataEncerramento": "",
                "Filtro": {}
            }
        self.headers= {
            "content-type": "application/json"
        }
        
    
    # def _getModelo(self, lote:BeautifulSoup):
    #     modelo = lote.find("h4", class_="itm-name")
    #     span = modelo.find('span')
    #     if span:
    #       span.extract() 
    #     return modelo.get_text(strip=True) if modelo else None
        
    # def _getMarca(self, lote:BeautifulSoup):
    #     marca = lote.find("span", class_="itm-marca")
    #     return marca.text if marca else None
    
    # def _getAno(self, title):
    #     ano_match = re.search(r"(\d{4}/\d{4})", title)
    #     return ano_match.group(1) if ano_match else None
    
    # def _getThumb(self, lote:BeautifulSoup):
    #     img_tag = lote.find("img", class_="item-imgsrc")
    #     return img_tag["src"] if img_tag else None
    
    # def _getLink(self, lote:BeautifulSoup):
    #     link_tag = lote.find("a", class_="itm-cdlink", href=True)
    #     return self.url + link_tag["href"] if link_tag else None
    
    # def _getLoteNumero(self, lote:BeautifulSoup):
    #   lote_num = lote.find("p", class_="itm-info")
    #   span = lote_num.find('span')
    #   if span:
    #     span.extract() 
    #   return lote_num.get_text(strip=True) if lote_num else None
      
    # def _getLanceInicial(self, lote:BeautifulSoup):
    #     try: 
    #         lance_inicial = lote.find("p", class_="itm-start")
    #         span = lance_inicial.find('span')
    #         if span:
    #           span.extract() 
    #         lance_inicial_text = lance_inicial.get_text(strip=True)
    #         return float(lance_inicial_text.replace("R$", "").replace(".", "").replace(",", "."))  if lance_inicial_text  else None 
    #     except Exception as e:
    #         return None
    
    
    def exec(self):
        url = "https://www.mgl.com.br/ApiFeatures/GetBusca/1/1/0"

        payload = {
            "RangeValores": 0,
            "Scopo": 0,
            "IgnoreScopo": 0,
            "OrientacaoBusca": 0,
            "Mapa": "",
            "Busca": "fiat",
            "ID_Categoria": 0,
            "ID_Estado": 0,
            "ID_Cidade": 0,
            "Bairro": "",
            "ID_Regiao": 0,
            "ValorMinSelecionado": 0,
            "ValorMaxSelecionado": 0,
            "CFGs": "[]",
            "Pagina": 1,
            "sInL": "",
            "Ordem": 0,
            "QtdPorPagina": 24,
            "SubStatus": [],
            "ID_Leiloes_Status": [],
            "PaginaIndex": 1,
            "BuscaProcesso": "",
            "NomesPartes": "",
            "CodLeilao": "",
            "TiposLeiloes": [],
            "PracaAtual": 0,
            "DataAbertura": "",
            "DataEncerramento": "",
            "Filtro": {}
        }
        headers = {"content-type": "application/json"}

        response = requests.get(url, json=payload, headers=headers)
        
        print(response.cookies)
        # print(response.text)s

        
        return []



