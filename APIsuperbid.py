import requests
import re  # Para expressões regulares


# Função para obter marcas de veículos da API FIPE
def obter_marcas_fipe():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

        else:
            print(f"Erro ao acessar a API FIPE: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao conectar à API FIPE: {e}")
        return []

def obter_modelos_fipe(codigo_marca):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Retornar apenas os nomes dos modelos
            return [modelo["nome"] for modelo in response.json()["modelos"]]
        else:
            print(f"Erro ao acessar a API FIPE: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao conectar à API FIPE: {e}")
        return []

def extrair_detalhes(title, marcas):
    ano_match = re.search(r"\b((19|20)?[0-9]{2}(/(19|20)?[0-9]{2})?)\b", title)
    ano = ano_match.group(0) if ano_match else None

    # Tentar identificar a marca com base na lista dinâmica
    marca_info = next((m for m in marcas if m['nome'].lower() in title.lower()), None)

    if marca_info:
        marca = marca_info['nome']
        codigo_marca = marca_info['codigo']
    else:
        marca = None
        codigo_marca = None

    if codigo_marca:
        modelos = obter_modelos_fipe(codigo_marca)
        modelo = next((m for m in modelos if m.lower() in title.lower()), None)
    else:
        modelo = None

    # Retornar os detalhes extraídos
    return marca, modelo, ano

def SuperBid(query):
    url = "https://api.sbwebservices.net/offer-query/seo/offers"

    querystring = {"keyword":query,"locale":"pt_BR","orderBy":"score:desc","pageNumber":"1","pageSize":"30",
                   "portalId":"[2,15]","requestOrigin":"marketplace","searchType":"opened",
                   "timeZoneId":"America/Sao_Paulo","urlSeo":"https://www.superbid.net/busca/"}
                   # ,"filter":"product.subCategory.category.description:carros"}

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

    # Obter marcas de veículos da API FIPE
    marcas = obter_marcas_fipe()

    if not marcas:
        print("Não foi possível obter marcas de veículos. Verifique a API.")
        # return []

    for item in data['offers']:
        template = item['product'].get('template', None)

        ano = ''
        marca = ''
        modelo = ''

        if template:
            for group in template['groups']:
                for property in group['properties']:
                    if property['id'] == 'anomodelo':
                        ano = property['value']
                    if property['id'] == 'marca':
                        marca = property['value']
                    if property['id'] == 'modelo':
                        modelo = property['value']
                        # break
                if ano:
                    break
        else:
            ano = ''

        descricao = item['product'].get('shortDesc', 'Descrição não disponível')

        # Verifica se há informção da monta na descrição do anuncio
        if 'pequena monta' in descricao.lower():
            monta = 'Pequena Monta'
        elif 'média monta' in descricao.lower():
            monta = 'Média Monta'
        elif 'grande monta' in descricao.lower():
            monta = 'Grande Monta'
        else:
            monta = ''

        # Extrair detalhes do título
        ret_marca, ret_modelo, ret_ano = extrair_detalhes(descricao, marcas)

        if not marca:
            marca = item['product']['brand'].get('description')
            if not marca:
                marca = ret_marca
        if not modelo:
            modelo = item['product']['model'].get('description')
            if not modelo:
                modelo = ret_modelo
        if not ano:
            ano = ret_ano
            if not ano:
                ano = 'NÃO DISPONIVEL'


        resultado = {
            "lote": item['lotNumber'],
            "marca": marca,
            "modelo": modelo,
            "monta": monta,
            "ano": ano,
            "thumb": item['product'].get('thumbnailUrl', 'Imagem não disponível'),
            "link": f"https://www.superbid.net/oferta/{item['id']}",
            "leiloeiro":"SuperBid"
        }

        if marca:
            print(resultado)
            resultados.append(resultado)

    return resultados