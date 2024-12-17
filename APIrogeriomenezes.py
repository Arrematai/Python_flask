import requests
from bs4 import BeautifulSoup
import json
import re  


# Função para obter marcas de veículos da API FIPE
def obter_marcas_fipe():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Retornar apenas os nomes das marcas
            return [marca["nome"] for marca in response.json()]
        else:
            print(f"Erro ao acessar a API FIPE: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao conectar à API FIPE: {e}")
        return []


# Função para extrair detalhes do título
def extrair_detalhes(title, marcas):
    # Padrão para anos, como "2022/2023" ou "2018"
    ano_match = re.search(r"\b(19[0-9]{2}|20[0-9]{2})(\/(19[0-9]{2}|20[0-9]{2}))?\b", title)
    ano = ano_match.group(0) if ano_match else None

    # Tentar identificar a marca com base na lista dinâmica
    marca = next((m for m in marcas if m.lower() in title.lower()), None)

    # Tentativa de capturar o modelo: removendo marca e ano, o restante pode ser o modelo
    modelo = title
    if marca:
        modelo = modelo.replace(marca, "").strip()
    if ano:
        modelo = modelo.replace(ano, "").strip()

    # Retornar os detalhes extraídos
    return marca, modelo, ano

# Função principal para processar os lotes
def rogeriomenezes(query):
    url = "https://www.rogeriomenezes.com.br/busca"
    querystring = {"interesse": query}

    headers = {
        'accept': "*/*",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        'x-requested-with': "XMLHttpRequest",
        'referer': "https://www.rogeriomenezes.com.br/",
        'origin': "https://www.rogeriomenezes.com.br"
    }

    # Realizar a requisição
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Erro ao acessar o site: Status {response.status_code}")
        return []

    # Obter marcas de veículos da API FIPE
    marcas = obter_marcas_fipe()
    if not marcas:
        print("Não foi possível obter marcas de veículos. Verifique a API.")
        return []

    # Parsear o HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar os itens
    resultados = []
    for resultado in soup.select(".lote-item"):
        try:
            # Capturar o título
            title = resultado.select_one("h3").get_text(strip=True)

            # Capturar o link completo e o lote
            link_tag = resultado.select_one("a.img-destaque")
            link = "https://www.rogeriomenezes.com.br" + link_tag["href"] if link_tag else None

            # Extrair o lote do link
            lote = link_tag["href"].split("/")[2] if link_tag else None

            # Capturar a imagem
            img_tag = resultado.select_one(".img img")
            img_url = img_tag["src"] if img_tag else None

            # Extrair detalhes do título
            marca, modelo, ano = extrair_detalhes(title, marcas)

            # Adicionar ao resultado
            resultados.append({
                "lote": lote,
                "marca": marca,
                "modelo": modelo,
                "monta" : "",
                "ano": ano,
                "thumb": img_url,
                "link": link,
                "leiloeiro":"Rogério Menezes"

            })
        except Exception as e:
            print(f"Erro ao processar um resultado: {e}")

    # Converter para JSON e exibir
    json_output = json.dumps(resultados, indent=4, ensure_ascii=False)
    # print(json_output)
    return resultados


