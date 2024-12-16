import requests
import re
from bs4 import BeautifulSoup
import json
import urllib3

# Desativando avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def Freitas(query):
    url = "https://www.freitasleiloeiro.com.br/Leiloes/PesquisarLotes"

    parametros = {
        "Nome": query,
        "Categoria": 1,
        "TipoLoteId": 0,
        "FaixaValor": 0,
        "Condicao": 0,
        "PatioId": 0,
        "AnoModeloMin": 0,
        "AnoModeloMax": 0,
        "ArCondicionado": "false",
        "DirecaoAssistida": "false",
        "ClienteSclId": 0,
        "PageNumber": 1,
        "TopRows": 12
    }

    headers = {
        'accept': "*/*",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
        'x-requested-with': "XMLHttpRequest"
    }

    resultados = []
    page_number = 1

    while True:
        parametros["PageNumber"] = page_number
        response = requests.get(url, params=parametros, headers=headers, verify=False)

        if response.status_code != 200:
            print(f"Erro ao acessar o site na página {page_number}: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        lotes = soup.find_all("div", class_="cardlote")

        if not lotes:
            print(f"Não há mais lotes na página {page_number}.")
            break

        for lote in lotes:
            title = lote.find("div", class_="cardLote-descVeic")
            title = title.get_text(strip=True) if title else ""

            # Extraindo marca e modelo
            marca_modelo_match = re.match(r"^(\w+)/([\w\s\.\-]+)", title)
            marca = marca_modelo_match.group(1) if marca_modelo_match else None
            modelo = marca_modelo_match.group(2).split(",")[0] if marca_modelo_match else None

            # Extraindo ano
            ano_match = re.search(r"(\d{2}/\d{2})", title)
            ano = ano_match.group(1) if ano_match else None

            img_tag = lote.find("img", class_="cardLote-img")
            thumb = img_tag["src"] if img_tag else None

            link_tag = lote.find("a", href=True)
            link = "https://www.freitasleiloeiro.com.br" + link_tag["href"] if link_tag else None

            # Extraindo o número do lote do final da URL
            lote_numero = re.search(r"loteNumero=(\d+)", link).group(1) if link else None

            # Extraindo a monta
            monta = None
            if link
                try:
                    detail_page_response = requests.get(link, headers=headers, verify=False)
                    if detail_page_response.status_code == 200:
                        detail_soup = BeautifulSoup(detail_page_response.text, "html.parser")
                        monta_tag = detail_soup.find("span", class_="fw-bold small")
                        if monta_tag:
                            monta_text = monta_tag.get_text(strip=True)
                            monta_match = re.search(r"(\w+)\s+MONTA", monta_text)
                            monta = monta_match.group(0) if monta_match else None
                except Exception as e:
                    print(f"Erro ao acessar página de detalhes: {e}")

            resultado = {
                "ano": ano,
                "leiloeiro": "Freitas Leiloeiro",
                "link": link,
                "lote": lote_numero,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "thumb": thumb               
            }

            resultados.append(resultado)

        page_number += 1

    # Imprimindo os resultados em formato JSON
    
    return resultados
