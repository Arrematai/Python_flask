import requests
from flask import jsonify


def SodreSantoro(query):
    url = "https://dc60842cf2f240e6b45f1f2db7f23641.sa-east-1.aws.found.io/veiculos/_search"

    payload = {
        "aggs": {
            "lot_financeable": {"terms": {
                    "field": "lot_financeable.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_category": {"terms": {
                    "field": "lot_category.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_origin": {"terms": {
                    "field": "lot_origin.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_sinister": {"terms": {
                    "field": "lot_sinister.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_brand": {
                "terms": {
                    "field": "lot_brand.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                },
                "aggs": {"lot_model": {"terms": {
                            "field": "lot_model.keyword",
                            "size": 200,
                            "order": {"_key": "asc"}
                        }}}
            },
            "client_name": {"terms": {
                    "field": "client_name.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_fuel": {"terms": {
                    "field": "lot_fuel.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_transmission": {"terms": {
                    "field": "lot_transmission.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_optionals": {"terms": {
                    "field": "lot_optionals.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }},
            "lot_location": {"terms": {
                    "field": "lot_location.keyword",
                    "size": 200,
                    "order": {"_key": "asc"}
                }}
        },
        "query": {"bool": {"must": [{"terms": {"lot_test": [0]}}, {"terms": {"lot_brand.keyword": [f"{query}"]}}]}},
        "from": 0,
        "sort": {
            "lot_status_id_order": {"order": "asc"},
            "auction_date_init": {"order": "asc"},
            "lot_number.keyword": {"order": "asc"}
        },
        "size": 48
    }
    headers = {
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "ApiKey d2NHYVRKRUI0R0s5Q2kwRXNfNGU6b0xGVDl3blFRd0t6S2hZVURKZThHZw==",
        "content-type": "application/json",
        "origin": "https://www.sodresantoro.com.br",
        "priority": "u=1, i",
        "referer": "https://www.sodresantoro.com.br/"
    }

    response = requests.post(url, data=payload, headers=headers)
    data = response.json()

    resultados = []

    for item in data.get('data', {}).get('results', {}).get('content', []):
        resultado = {
            "lote": item.get("lot_id"),
            "marca": item.get("lot_brand"),
            "modelo": item.get("lot_model"),
            "monta": item.get("lot_sinister"),
            "ano": item.get("lot_year_manufacture"),
            "thumb": item.get("lot_pictures")[0].replace("\\/", "/") if item.get("lot_pictures") else None,
            "link": "https://leilao.sodresantoro.com.br/leilao/" + str(item.get("auction_id")) + "/lote/" + str(
                item.get("lot_id")) + "/?ref=v2"
        }
        # Adiciona o dicionário à lista de resultados
        resultados.append(resultado)

    # Exibe os resultados
    print(resultados)
    # return jsonify(resultados)
    return resultados