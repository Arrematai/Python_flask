import os
# import logging
import re
from typing import Text
from flask import json
import requests
import uuid

from src.infra.helpers.MarcaCarros import obter_marcas, replace_marcas
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log


class ServiceRigolon:
    url: Text = 'https://www.rigolonleiloes.com.br/core/api/get-lotes'
    # url: Text = 'https://www.rigolonleiloes.com.br'
    params: Text
    headers: Text
    

    def __init__(self, query, size, api):
        self.query = query
        self.size = size
        self.api = api
        self.Marcas = obter_marcas()
        self.resultados = []
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.url = f"{self.url}?tipo=1&palavra_chave={self.query}"
        self.headers= {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Cookie": "PHPSESSID=545hs3b048s4rtcqsfde286jl1",
            "Origin": "https://www.rigolonleiloes.com.br",
            "Referer": "https://www.rigolonleiloes.com.br",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        }
        
    # Regex para capturar o modelo
    def _getModelo(self, marca_modelo, marca):
        padrao = rf'{re.escape(marca)}[ /]([a-zA-Z0-9\s.]+)'
        match = re.search(padrao, marca_modelo, re.IGNORECASE)
        if match:
            modelo = match.group(1).strip()
            return modelo
        return None
    
    def _getAno(self, marca_modelo):
        match = re.search(r"(\d{2}\/\d{2}|\d{4}\/\d{4})", marca_modelo)
        if match:
            return match.group(1).strip()
        
    def exec (self):
        items = []
        response = requests.post(self.url, headers=self.headers, verify=False)
                
        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": self.resultados, "http_code": response.status_code }
        
        
        data = response.json()
        
        if data:
            items = data.get("items")
            
            for item in items:
                lote = item["lote_id"]
                leilao = item["leilao_id"]
                monta = getMonta("")
                marca_modelo = replace_marcas(item["nm_titulo_lote"]) #"nm_titulo_lote": "Fiat/Palio ED - 96/97 – Três Corações/MG",
                marca = re.split(r'[ /]', marca_modelo)[0]
                modelo = self._getModelo(marca_modelo, marca)
                ano = self._getAno(marca_modelo)
                valor_atual = item["vl_lanceinicial"]
                link = f"https://www.rigolonleiloes.com.br/leilao/index/leilao_id/{leilao}/lote/{lote}"
                thumb = item["fotos"][0]["nm_path_completo"] if "fotos" in item and isinstance(item["fotos"], list) and len(item["fotos"]) > 0 else None
                
                
                
                resultado = {
                    "uuid": str(uuid.uuid4()),
                    "lote": lote,
                    "chassi": None,
                    "valor_fipe": None,
                    "valor_atual": valor_atual,
                    "tipo_veiculo": "",
                    "marca": marca,
                    "modelo": modelo,
                    "monta": monta,
                    "ano": ano,
                    "thumb": thumb ,
                    "link": link,
                    "leiloeiro":"Rigolon Leilões",
                    "ativo": 1,
                }
                
                self.resultados.append(resultado)   
        

        # Exibe os resultados
        # print(len(resultados))
        # return jsonify(resultados)
        return { "resultados": self.resultados, "http_code": response.status_code }
