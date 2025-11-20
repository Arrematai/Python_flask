import os
# import logging
import re
from typing import Text
import requests
import uuid
from requests.exceptions import HTTPError

from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log



class ServicePestana:
    url: Text = 'https://www.pestanaleiloes.com.br/api/v2/lote'
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
        
    def initValue(self):
        self.headers= {}
        
    def _getModelo(self, descricao:str):
        padrao = re.compile(
            r"(?:Sucata\s+)?Fiat\s+(.*?)\s+\d{4}\s+\d{4}",
             re.VERBOSE | re.IGNORECASE
        )
        match = padrao.search(descricao)
        if match:
            modelo = match.group("modelo").strip(" ,.-").title()
            #print(f"✅ Success: {loteNome}")
            return modelo
        else:
            #print(f"⚠️ Error: {loteNome}")
            return None
        
    def exec (self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": self.resultados, "http_code": response.status_code }
        
          
        data = response.json()
        
        
        automoveis = list(filter(lambda item: item["bens"][0]["tipoBem"]["id"] == 421, data))
        
        
        if automoveis and len(automoveis) > 0:
          for automovel in automoveis:
              
              
            descricao = automovel.get("descricao")
            valor_atual = automovel.get("valorInicial")
            leilao = automovel.get("leilao")
            lote = automovel.get("id")
            link = f"https://www.pestanaleiloes.com.br/agenda-de-leiloes/{leilao}/{lote}"
            

            thumb = None
            try:
                thumb = automovel["bens"][0]["imagens"][0]["original"]
            except (KeyError, IndexError, TypeError):
                thumb = None
            
            
            
            if descricao and self.query.lower() in descricao.lower():
                
                padrao = re.compile(
                    r"^(?:-?\s*Sucata\s+)?(?P<marca>[A-Z][a-zçéèãâêôí]+)\s+(?P<modelo>.*?)\s+(?P<ano1>\d{4})(?:\s+(?P<ano2>\d{4}))?\s+(?P<combustivel>[A-Za-z/çéÉãÃôÔíÍ\s]+)$",
                    re.IGNORECASE
                )
                
                for linha in descricao.strip().splitlines():
                    m = padrao.search(linha.strip())
                    if m:
                        resultado = {
                            "uuid": str(uuid.uuid4()),
                            "lote":  lote,
                            "chassi": "",
                            "valor_fipe": None,
                            "valor_atual": valor_atual,
                            "tipo_veiculo": "",
                            "marca": m.group("marca"),
                            "modelo": m.group("modelo").strip(),
                            "monta": getMonta(None),
                            "ano": f'{m.group("ano1")}/{m.group("ano2")}',
                            "thumb": f"https://ged.pestanaleiloes.com.br/ged/{thumb}",
                            "link": link,
                            "combustivel": m.group("combustivel").strip(),
                            "leiloeiro":"Pestana Leilões",
                            "ativo": 1,
                        }

              
                        self.resultados.append(resultado)

        # Exibe os resultados
        # print(len(self.resultados))
        # return jsonify(resultados)
        return { "resultados": self.resultados, "http_code": response.status_code }
