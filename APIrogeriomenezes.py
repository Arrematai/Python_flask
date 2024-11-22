import requests
from bs4 import BeautifulSoup
import json

def rogeriomenezes(query):

    url = "https://www.rogeriomenezes.com.br/busca"

    querystring = {"interesse" : f"{query}"}

    payload = ""
    headers = {"User-Agent": "insomnia/10.1.1"}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    # Parsear o HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar os itens
    lotes = []
    for lote in soup.select(".lote-item"):
        try:
            title = lote.select_one("h3").text.strip()
            img_url = lote.select_one(".img img")["src"]
            link = "https://www.rogeriomenezes.com.br" + lote.select_one("a.img-destaque")["href"]
            description = lote.select_one(".info p").text.strip() if lote.select_one(".info p") else None

            lotes.append({
                "title": title,
                "thumb": img_url,
                "link": link,
                "description": description
            })
        except Exception as e:
            print(f"Erro ao processar um lote: {e}")

    # Converter para JSON e exibir
    json_output = json.dumps(lotes, indent=4, ensure_ascii=False)
    print(json_output)


rogeriomenezes("ford")