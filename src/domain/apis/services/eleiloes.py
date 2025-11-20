import os
# import logging
import re
from bs4 import BeautifulSoup, Tag
from typing import Any, Text
import requests
import uuid
from requests.exceptions import HTTPError

from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log



class ServiceEleiloes:
    url: Text = "https://www.e-leiloes.com.br"
    payload: Text
    headers: Text
    resultados: list = []

    def __init__(self, query: str, size: int, api = None):
        self.query = query
        self.size = size
        self.api = api
        self.resultados = []
        self.initValue()
        self.log = Log("")
        self.currPage = 1
        
    def initValue(self):
        self.headers= {}
        
    def _getThumb(self, lote):
        img_tag = lote.select_one("a.lote-thumb")
        img_url = None
        if img_tag and img_tag.has_attr("style"):
            match = re.search(r"url\(['\"]?(.*?)['\"]?\)", img_tag["style"])
            if match:
                img_url = match.group(1)
        return img_url
    
    def _getTitle(self, lote: Tag | Any):
        titulo = lote.select_one("h5.heading-5-copy a") or lote.select_one("a")
        return titulo.get_text(strip=True) if titulo else None
    
    def _getLink(self, lote: Tag | Any):
        titulo = lote.select_one("h5.heading-5-copy a") or lote.select_one("a")
        return titulo.get("href") if titulo else None
    
    def _getMarca(self, lote):
        padrao = re.compile(
            r"""^\s*
                (?P<marca>[A-Za-z0-9&\.\-]+)      # marca (ex: FIAT)
                [/\s]+
                (?P<modelo>                       # modelo: captura até ano, '-' ou fim da linha
                    .*?
                )
                (?=                               # lookahead: modelo termina antes de...
                    \s+\d{4}(?:/\d{4})?           #  - um ano (2008) ou 2008/2008
                    |\s*-\s*                      #  - ou " - " (cor, obs.)
                    |$                            #  - ou fim da linha
                )
                (?:\s+(?P<ano>\d{4}(?:/\d{4})?))?  # ano opcional
                (?:\s*-\s*(?P<cor>.+))?            # cor opcional após " - "
                \s*$""",
            re.IGNORECASE | re.VERBOSE,
        )
        for linha in lote.strip().splitlines():
            linha = linha.strip()
            m = padrao.search(linha)
            if m:
                marca = m.group("marca").upper().strip()
                modelo = (m.group("modelo") or "").strip(" -/")
                ano = (m.group("ano") or "").strip()
                return {
                    "marca": marca,
                    "modelo": modelo,
                    "ano": ano,
                }
    
    def _getLote(self, lote: Tag):
        info_div = lote.select_one(".infoLote")
        for s in info_div.select("strong"):
            s.extract()
        texto = info_div.get_text(" ", strip=True) or None
        m = re.search(r"Lote\s*-\s*(\d+)", texto)
        return m.group(1) if m else None
    
    def _getValor(self, lote: Tag):
        # Seleciona o bloco que contém o texto "Valor avaliado"
        avaliado_div = lote.select_one(".text-block-6 .text-span-1")

        valor_avaliado = None
        if avaliado_div:
            return avaliado_div.get_text(strip=True)
            
    def _getRequest(self):
        response = requests.get(f"{self.url}&page={self.currPage}")
        
        # response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": self.resultados, "http_code": response.status_code }
        
        lotes_html = response.content

        return BeautifulSoup(lotes_html, "html.parser")
        
    def exec (self):
        
        self.url = f"{self.url}/leilao/automoveis?busca={self.query}"
        
        soup = self._getRequest()
        pages = soup.find("ul", class_="default-pagination") 
        pagesNumbers = [int(span.get_text(strip=True)) for span in pages.find_all("span")] 
        
        
        for page in pagesNumbers:
            lotes = []
            
            if page == 1:
                lotes = soup.find_all("div", class_="item-list lote-item")
            else:
                self.currPage = page
                soup = self._getRequest()
                lotes = soup.find_all("div", class_="item-list lote-item")
            
            for lote in lotes:
                title = self._getTitle(lote)
                link =  self._getLink(lote)
                thumb =  self._getThumb(lote)
                valores =  self._getMarca(title)
                ano = valores["ano"] or None
                marca = valores["marca"] or None
                modelo = valores["modelo"] or None
                numberLote = self._getLote(lote)
                resultado = {
                    "uuid": str(uuid.uuid4()),
                    "lote":  numberLote,
                    "chassi": "",
                    "valor_fipe": None,
                    "valor_atual": self._getValor(lote) or None,
                    "tipo_veiculo": "",
                    "marca": marca,
                    "modelo": modelo,
                    "monta": getMonta(None),
                    "ano": ano,
                    "thumb": thumb,
                    "link": f"https://www.e-leiloes.com.br{link}",
                    "leiloeiro":"E-Leilões",
                    "ativo": 1,
                }
                self.resultados.append(resultado)

        # Exibe os resultados
        # print(len(self.resultados))
        # return jsonify(resultados)
        return { "resultados": self.resultados, "http_code": 200 }
