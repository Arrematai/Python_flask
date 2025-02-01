import os
# import logging
import re
from typing import Text
import requests
import uuid
from bs4 import BeautifulSoup

from src.infra.helpers.Monta import getMonta

class ServiceLiderLeiloes:
    url: Text = 'https://www.liderleiloes.com.br'
    payload: Text
    headers: Text
    resultados: list = []

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.resultados = []
        self.initValue()
    
    def initValue(self):
      self.url = f'{self.url}/busca?busca={self.query}'
      self.headers= {
          'accept': "*/*",
          'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
          'x-requested-with': "XMLHttpRequest",
          "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
      }
      
    def _getTitle(self, lote: BeautifulSoup):
        title = lote.find("h3")
        return title.get_text(strip=True) if title else None
    
    def _getModelo(self, title):
        modelo_match = re.match(r"^(\w+)/([\w\s\.\-]+)", title)
        return modelo_match.group(2).split(",")[0] if modelo_match else None
        
    def _getMarca(self, title):
        marca_match = re.match(r"^(\w+)/([\w\s\.\-]+)", title)
        return marca_match.group(1) if marca_match else None
    
    def _getAno(self, title):
        ano_match = re.search(r"(\d{4}/\d{4})", title)
        return ano_match.group(1) if ano_match else None
      
    def _getThumb(self, lote):
        img_tag = lote.find("img")
        return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote):
        link_tag = lote.find("a", href=True)
        return self.url + link_tag["href"] if link_tag else None
    
    def _getLoteNumero(self, link):
      try:
        return re.search(r"veiculos/.+?/(\d+)/", link).group(1) if link else None
      except Exception as e:
        return None
          
    def _getValorAtual(self, page_lote):
        try: 
            valor_atual = page_lote.find("div", class_="c-left")
            valor_atual = valor_atual.get_text(strip=True)
            return float(valor_atual.replace("R$", "").replace(".", "").replace(",", "."))  if valor_atual  else None
        except Exception as e:
            return None
    
        
    def exec (self):
        response = requests.get(self.url, headers=self.headers)
        
        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            print(f"Erro ao acessar o site na página: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        lotes = soup.find_all("article")
        
      
        
        for lote in lotes:
          monta = "Não Informado"
          title = self._getTitle(lote)
          marca = self._getMarca(title)
          modelo = self._getModelo(title)
          ano = self._getAno(title)
          thumb = self._getThumb(lote)
          link = self._getLink(lote)
          lote_numero = self._getLoteNumero(link)
          valor_atual = self._getValorAtual(lote)
          
      
          resultado = {
              "uuid": str(uuid.uuid4()),
              "lote": lote_numero,
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
              "leiloeiro":"Lider Leilões",
              "ativo": 1,
          }
      

          self.resultados.append(resultado)

        # # Exibe os resultados
        # # print(len(resultados))
        # # return jsonify(resultados)
        return self.resultados