import http.client
import json
import re  

def Rigolon(query):
    conn = http.client.HTTPSConnection("www.rigolonleiloes.com.br")

    # O payload contém os parâmetros para a busca
    payload = f"pg=1&tipo=&categoria=&estado=&cidade=&palavra_chave={query}"

    # Definindo os headers para a requisição
    headers = {
        'Accept': "*/*",
        'Accept-Language': "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': "PHPSESSID=apumcprsek18lqg5d1uk6cnl7n",  # Substitua pela sessão atual se necessário
        'Origin': "https://www.rigolonleiloes.com.br",
        'Referer': "https://www.rigolonleiloes.com.br/",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
        'X-Requested-With': "XMLHttpRequest",
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Opera GX";v="114"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"'
    }

    resultados = []

    # Fazendo a requisição POST
    conn.request("POST", "/core/api/get-lotes", payload, headers)

    # Obtendo a resposta da requisição
    res = conn.getresponse()
    data = res.read()

    # Decodificando e transformando a resposta em JSON
    try:
        response_data = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON!")
        return []

    # Obtendo os itens da resposta
    items = response_data.get('items', [])
    if not items:
        print("Nenhum item encontrado na resposta.")
        return []

    # Filtrando e processando os resultados conforme solicitado
    for item in items:
        # Extraindo informações
        titulo_lote = item.get("nm_titulo_lote", "")
        ano_match = re.search(r'(\d{2}/\d{2})', titulo_lote)
        ano = ano_match.group(0) if ano_match else None

        # Ajustando a expressão regular para extrair marca e modelo corretamente
        marca_modelo_match = re.match(r'([A-Za-z]+)/(.+?)\s*-\s*\d{2}/\d{2}', titulo_lote)
        marca = marca_modelo_match.group(1) if marca_modelo_match else None
        modelo = marca_modelo_match.group(2).strip() if marca_modelo_match else None

        thumb_list = item.get("fotos", [])
        thumb_url = thumb_list[0].get("nm_path_completo") if thumb_list and "nm_path_completo" in thumb_list[0] else None

        # Criando o resultado no formato desejado
        if modelo:
            resultado = {
                "lote": item.get("lote_id"),
                "marca": marca,
                "modelo": modelo,
                "monta": "",
                "ano": ano,
                "thumb": thumb_url,
                "link": f"https://www.rigolonleiloes.com.br/leilao/index/leilao_id/{item.get('leilao_id')}/lote/{item.get('lote_id')}",
                "leiloeiro":"Rigolon"
            }

        resultados.append(resultado)
    return resultados
            # # Exibindo o resultado
            # print(json.dumps(resultado, indent=2, ensure_ascii=False))


