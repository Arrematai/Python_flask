import os
# import logging
from typing import Text
import requests
import uuid


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
            "cookie": "copartbrmember=00df814ca4b576071d1e8881929849e1",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        }
        
    def exec (self):
        response = requests.post(self.url, headers=self.headers)
        
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
                "monta": monta,
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
