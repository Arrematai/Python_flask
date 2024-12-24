import requests
import re
import http.client
import json

from FlaskTESTE import query


def MGL():

    url = "https://api.scraperapi.com/"

    payload = {
        "RangeValores": 0,
        "Scopo": 0,
        "IgnoreScopo": 0,
        "OrientacaoBusca": 0,
        "Mapa": "",
        "Busca": f"{query}",
        "ID_Categoria": 0,
        "ID_Estado": 0,
        "ID_Cidade": 0,
        "Bairro": "",
        "ID_Regiao": 0,
        "ValorMinSelecionado": 0,
        "ValorMaxSelecionado": 0,
        "CFGs": "[]",
        "Pagina": 1,
        "sInL": "",
        "Ordem": 0,
        "QtdPorPagina": 24,
        "SubStatus": [],
        "ID_Leiloes_Status": [],
        "PaginaIndex": 1,
        "BuscaProcesso": "",
        "NomesPartes": "",
        "CodLeilao": "",
        "TiposLeiloes": [],
        "PracaAtual": 0,
        "DataAbertura": "",
        "DataEncerramento": "",
        "Filtro": {},
        'api_key': 'ea244fae842ba85e93fd4ee8f83b2672',
        'url': 'https://www.mgl.com.br/ApiFeatures/GetBusca/1/1/0',
        'country_code': 'us',
        'device_type': 'desktop'
    }
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        'content-type': "application/json; charset=UTF-8",
        'cookie': "_fbp=fb.2.1718765809662.368449749229942804; _ga=GA1.1.2059919323.1718765810; rdtrk=%7B%22id%22%3A%22d974f498-a165-4cb7-b137-a6fbaa34722c%22%7D; cookieconsent_status_UNCATEGORIZED=DISMISS; cookieconsent_status_ESSENTIAL=DISMISS; cookieconsent_status_PERSONALIZATION=DISMISS; cookieconsent_status_ANALYTICS=DISMISS; cookieconsent_status_MARKETING=DISMISS; _gcl_au=1.1.970901919.1726802702; .Web.LeiloesApp.1.0=CfDJ8OqWaofM7hZChJ2QSEYwvrUXDLxdJCepJ7p1P2i6srMQ9WeZ9NvQbR3Ngl6IQzD4iXiApurPv28SieaHReG1NiitxUho7FBNw3QdQ6npqbELxi1WEYa2iN%2BRhdGli4v5s%2FnNxzGWIc%2Bb5AiLXyyLRHJEwcdxAX7DZ4lb2EA%2FpKg7; WCL.Atf=CfDJ8EZWcPR2GZdKi84Rm5RoLxEpcQfnFhdtLGcd7FfRRSgtE4HCMQSz1Tg0gupXKczNekmK7TPydWPa2HJOK27Q_ceLc0TY7p_ODKrjhBYzhIKuVo-t13sswjGINZ8SRqywGD5sdaj5KnqMPW2j9BfQn_M; _ga_ZQ6VT30XKY=GS1.1.1731379332.7.1.1731380494.30.0.0; cf_clearance=NlZ_Mj2.gorIPlvxQJlUfc3GAKRtjHmNZlrICErpf0o-1731380494-1.2.1.1-bfn.YJMYWeDhVeFtGu3cfZLwwVwApTKBDTbdq2OcFRob5O_oOd9sE2vB1Xi7tXr.mnMOe4YxUjz1E1FsHzTb5O3PQS2PKj70zXZ0sw5gwsZkC04LyRIhfS4R5r1Ym7man04v4oGhGaqmNutIAvpd.ZMMQIPgLZJdImX.6bVdZLZMMOXIgmRL5FgWjwJBiE.wzjY9DOxUhLIE7aGu.dTnTIWCsIQqtGiTy9cU.iSOq9.iUog8F96IsNX39XKrGrT16RoasHXtFZZnYUKTPJXuaRA0AidFZOOVb3w80TD3tetLWsZmuUzpzf_bhp0vvFLtgTUtz.VPbcJfAZgKXFsSLcR0obGjpXCVFv45g_tSMB38N51fwMCc6qrC2YANEzruGbq_pXQz0kfHbdtLJpFJWa057gN.ndb5A1GyKxZ1COc; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3JlYXRlZF9hdCI6MTczMTM4MDQ5NDc4OH0=; _ga_SVB3JJTM93=GS1.1.1731375310.6.1.1731380611.60.0.0; CookiesChaveCliente=30baeb47071c4d5383da58ede87576feupBWIyNCPiiRZEBBlHdOjTBIPEROXAkvwxVPjEaQCwfKdIXVePRpbUiantGDgyfOymUcimSggNLnorfHb898e24470be477aa0be55b0fbf9cf9a; CookiesChaveClienteUL=30baeb47071c4d5383da58ede87576feupBWIyNCPiiRZEBBlHdOjTBIPEROXAkvwxVPjEaQCwfKdIXVePRpbUiantGDgyfOymUcimSggNLnorfHb898e24470be477aa0be55b0fbf9cf9a; CookiesUserIsHomologacao=",
        'origin': "https://www.mgl.com.br",
        'priority': "u=1, i",
        'referer': "https://www.mgl.com.br/",
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not A Brand";v="99"',
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        'x-requested-with': "XMLHttpRequest"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200 or not response.headers.get("Content-Type", "").startswith("application/json"):
        print("Erro na resposta da API ou resposta não é JSON.")
        print("Código de status:", response.status_code)
        print("Conteúdo da resposta:", response.text)  # Exibe o conteúdo para inspeção
        return []

    print(response)
    data = response.json()



    resultados = []
    for item in data.get('Lotes', []):
        descricao = item.get("Lote", "")
        extracao = extrair_dados(descricao)

        resultado = {
            "lote": item.get("LoteNumero"),
            "marca": extracao["marca"],
            "modelo": extracao["modelo"],
            "monta": "No estado e condições que se encontra",
            "ano": extracao["ano"],
            "thumb": "https://www.mgl.com.br/imagens-center/350x282/" + item.get("Foto"),
            "link": "https://www.mgl.com.br/" + str(item.get("URLlote")),
            "leiloeiro":"MGL"
        }
        # Adiciona o dicionário à lista de resultados
        resultados.append(resultado)

    # Exibe os resultados
    print(resultados)
    # return jsonify(resultados)
    return resultados

def extrair_dados(descricao):
    # Define regex para capturar o ano no formato AAAA/AAAA
    ano_match = re.search(r'(\d{4})/(\d{4})', descricao)
    ano = ano_match.group(2) if ano_match else None  # Pega o segundo ano, se presente

    # Separa a descrição antes do ano
    parte_inicial = descricao[:ano_match.start()] if ano_match else descricao

    # Encontra a marca e o modelo como as duas primeiras palavras após o hífen, barra ou espaço
    marca_modelo_match = re.search(r'-?\s*([\w]+)[/\s]+([\w]+)', parte_inicial)
    marca = marca_modelo_match.group(1) if marca_modelo_match else None
    modelo = marca_modelo_match.group(2) if marca_modelo_match else None

    return {"marca": marca, "modelo": modelo, "ano": ano}
MGL("bmw")