import os
# import logging
import re
from typing import Text
import requests
import uuid
from bs4 import BeautifulSoup

from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log

class ServiceLeilaoVip:
    url: Text = 'https://www.leilaovip.com.br'
    payload: Text
    headers: Text
    resultados: list = []

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.resultados = []
        self.log = Log("")
        self.initValue()
    
    def initValue(self):
      self.url = f'{self.url}/pesquisa/index?handler=pesquisar&Filtro.Texto={self.query}&Filtro.CategoriaId=3170e50e-7ad7-46ce-989a-b1880160be94'
      self.headers= {
          'accept': "*/*",
          'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
          'x-requested-with': "XMLHttpRequest",
          "Cookie": "ARRAffinity=76fd3b268e3639ef5cc726b99114e20afacd63341ee4df2a9e89cb8ea1f3ed4a; ARRAffinitySameSite=76fd3b268e3639ef5cc726b99114e20afacd63341ee4df2a9e89cb8ea1f3ed4a; __CBCanal=%7B%22CanalId%22%3A%225c4eeef5-df48-4f7d-939d-b18801602a48%22%7D"
      }
      
    def _getTitle(self, lote: BeautifulSoup):
      title = lote.find("h1")
      return title.get_text(strip=True) if title else None
    
    def _getModelo(self, title):
        modelo_match = re.match(r"\b(\w+[\s/]\w+.*?)(?=, ano)", title)
        modelo = modelo_match.group(1) if modelo_match else None
        
        if modelo:
          return [re.sub(r"^\w+[ /]", "", modelo)][0]
        else:
          return None
        
    def _getMarca(self, title):
        marca_match = re.match(r"^(\w+)", title)
        return marca_match.group(1) if marca_match else None
    
    def _getAno(self, title):
        ano_match = re.search(r'\b(\d{2,4})\b', title)
        return ano_match.group(1) if ano_match else None
      
    def _getThumb(self, lote):
        img_tag = lote.find("img")
        return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote):
        link_tag = lote.find("a", href=True)
        return self.url + link_tag["href"] if link_tag else None
    
    def _getValorAtual(self, page_lote):
        try: 
            valor_atual = page_lote.find("span", class_="valor-atual")
            valor_atual = valor_atual.get_text(strip=True)
            return float(valor_atual.replace("R$", "").replace(".", "").replace(",", "."))  if valor_atual  else None
        except Exception as e:
            return None
    
        
    def exec (self):
        response = requests.post(self.url, headers=self.headers)
        
        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": resultados, "http_code": response.status_code }
            

        soup = BeautifulSoup(response.text, "html.parser")
        lotes = soup.select("div.card-anuncio")
        
        for lote in lotes:
            monta = getMonta("")
            title = self._getTitle(lote)            
            marca = self._getMarca(title)
            modelo = self._getModelo(title)
            ano = self._getAno(title)
            thumb = self._getThumb(lote)
            link = self._getLink(lote)
            valor_atual = self._getValorAtual(lote)

            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": None,
                "chassi": None,
                "valor_fipe": None,
                "valor_atual": valor_atual,
                "tipo_veiculo": None,
                "marca": marca,
                "modelo": modelo,
                "monta": getMonta(monta),
                "ano": ano,
                "thumb": thumb,
                "link": link,
                "leiloeiro":"Leilão Vip",
                "ativo": 1,
            }

            self.resultados.append(resultado)

        return { "resultados": self.resultados, "http_code": response.status_code }