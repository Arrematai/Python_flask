from itertools import product

import requests


def SuperBid(query):
    url = "https://api.sbwebservices.net/offer-query/seo/offers"

    querystring = {"keyword":query,"locale":"pt_BR","orderBy":"score:desc","pageNumber":"1","pageSize":"30","portalId":"[2,15]","requestOrigin":"marketplace","searchType":"opened","timeZoneId":"America/Sao_Paulo","urlSeo":"https://www.superbid.net/busca/"}

    payload = ""
    headers = {
        "cookie": "__cf_bm=uobWTAu9HGNs8HVe4LFfSr1uU2W1pM8pp05snOTmXd4-1732108079-1.0.1.1-SFNI8XXgCwlC8wsUbAESqamToXss3KrQEAwFYWqFP3AfeQ48xp_qVG4RIGrZLpa5oftmYaRRRc4MNnRQZCpKDA",
        "accept": "application/json, application/hal+json",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pt-PT;q=0.5",
        "authorization": "",
        "client_id": "dzqC3VodSoXukD45BQKg3NQU6-faststore",
        "origin": "https://www.superbid.net",
        "priority": "u=1, i",
        "referer": "https://www.superbid.net/",
        "sec-ch-ua": """Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24""",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "suppress-authenticate": "true",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    data = response.json()

    resultados = []

    for item in data['offers']:
        template = item['product'].get('template', None)

        ano = 'Não disponível'
        if template:
            for group in template['groups']:
                for property in group['properties']:
                    if property['id'] == 'anomodelo':
                        ano = property['value']
                        break
                if ano:
                    break
        else:
            ano = 'Não disponível'

        resultado = {
            "lote": item['lotNumber'],
            "marca": item['product']['brand'].get('description', 'Não disponível'),
            "modelo": item['product']['model'].get('description', 'Não disponível'),
            "monta": '',
            "ano": ano,
            "thumb": item['product'].get('thumbnailUrl', 'Imagem não disponível'),
            "link": f"https://www.superbid.net/oferta/{item['id']}",
            # "Descrição": item['product'].get('detailedDescription', 'Descrição não disponível')
        }

        print(resultado)

        resultados.append(resultado)

    print('Resultados:', resultados)
    return resultados


