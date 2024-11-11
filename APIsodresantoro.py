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
        "referer": "https://www.sodresantoro.com.br/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    # print(data)

    resultados = []

    for item in data.get('hits', {}).get('hits', []):
        source = item.get('_source', {})

        resultado = {
            "lote": source.get("lot_id"),
            "marca": source.get("lot_brand"),
            "modelo": source.get("lot_model"),
            "monta": source.get("lot_sinister"),
            "ano": source.get("lot_year_manufacture"),
            "thumb": source.get("lot_pictures")[0] if source.get("lot_pictures") else None,
            "link": f"https://leilao.sodresantoro.com.br/leilao/{source.get('auction_id')}/lote/{source.get('lot_id')}/?ref=v2"

        }# Adiciona o dicionário à lista de resultados
        resultados.append(resultado)

    # Exibe os resultados
    print(resultados)
    # return jsonify(resultados)
    return resultados
