import os
# import logging
from typing import Text
import requests
import uuid

class ServiceSantoro:
    url: Text = "https://dc60842cf2f240e6b45f1f2db7f23641.sa-east-1.aws.found.io/veiculos/_search"
    payload: Text
    headers: Text
    
    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
    
    def initValue(self):
        self.payload = {
        "aggs": {
            "lot_financeable": {"terms": {
                "field": "lot_financeable.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_category": {"terms": {
                "field": "lot_category.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_origin": {"terms": {
                "field": "lot_origin.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_sinister": {"terms": {
                "field": "lot_sinister.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_brand": {
                "terms": {
                    "field": "lot_brand.keyword",
                    "size": self.size,
                    "order": {"_key": "asc"}
                },
                "aggs": {"lot_model": {"terms": {
                    "field": "lot_model.keyword",
                    "size": self.size,
                    "order": {"_key": "asc"}
                }}}
            },
            "client_name": {"terms": {
                "field": "client_name.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_fuel": {"terms": {
                "field": "lot_fuel.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_transmission": {"terms": {
                "field": "lot_transmission.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_optionals": {"terms": {
                "field": "lot_optionals.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }},
            "lot_location": {"terms": {
                "field": "lot_location.keyword",
                "size": self.size,
                "order": {"_key": "asc"}
            }}
        },
        "query": {"bool": {"must": [{"terms": {"lot_test": [0]}}, {"terms": {"lot_brand.keyword": [f"{self.query}"]}}]}},
        "from": 0,
        "sort": {
            "lot_status_id_order": {"order": "asc"},
            "auction_date_init": {"order": "asc"},
            "lot_number.keyword": {"order": "asc"}
        },
        "size": self.size
    }
        self.headers = {
            "accept": "application/json",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "ApiKey d2NHYVRKRUI0R0s5Q2kwRXNfNGU6b0xGVDl3blFRd0t6S2hZVURKZThHZw==",
            "content-type": "application/json",
            "origin": "https://www.sodresantoro.com.br",
            "priority": "u=1, i",
            "referer": "https://www.sodresantoro.com.br/",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
        }

    def exec(self):
        response = requests.post(self.url, json=self.payload, headers=self.headers)
        data = response.json()
        # print(data)

        resultados = []

        for item in data.get('hits', {}).get('hits', []):
            source = item.get('_source', {})
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": source.get("lot_id"),
                "chassi": None,
                "valor_fipe": None,
                "valor_atual":  source.get("bid_actual"),
                "tipo_veiculo": source.get("lot_category"),
                "marca": source.get("lot_brand"),
                "modelo": source.get("lot_model"),
                "monta": source.get("lot_sinister"),
                "ano": source.get("lot_year_manufacture"),
                "thumb": source.get("lot_pictures")[0] if source.get("lot_pictures") else None,
                "link": f"https://leilao.sodresantoro.com.br/leilao/{source.get('auction_id')}/lote/{source.get('lot_id')}/?ref=v2",
                "leiloeiro":"Sodré Santoro",
                "ativo": 1,

            }# Adiciona o dicionário à lista de resultados
            resultados.append(resultado)

        # Exibe os resultados
        print(len(resultados))
        return resultados
    
