import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import jsonify


def Palacio_dos_leiloes(query):


    url = "https://www.palaciodosleiloes.com.br/site/camada_ajax/coluna_esquerda_m.php"

    querystring = {f"quebra": "0.9389920978354351", "opcao": "listar_lote", "categoria_pesquisa": "",
                   "subcategoria_pesquisa": "", "marca_pesquisa": "", "situacao_pesquisa": "", "local_pesquisa": "",
                   "modelo_pesquisa": "", "ano_pesquisa": "", "grupo_site_pesquisa": "", "txt_pesquisa_lote": f"{query}",
                   "leilao_pesquisa": "", "tipo_exibicao": "grid", "paginacao": "0", "total_paginas": "1",
                   "somente_pesquisa": "0", "e_categoria": "1", "e_leilao": "1", "e_subcategoria": "0", "e_marca": "0",
                   "e_modelo": "0", "e_ano": "0", "e_situacao": "0", "e_local": "0", "e_grupo": "0"}

    payload = f"=&opcao=listar_lote&categoria_pesquisa=&subcategoria_pesquisa=&marca_pesquisa=&situacao_pesquisa=&local_pesquisa=&modelo_pesquisa=&ano_pesquisa=&grupo_site_pesquisa=&txt_pesquisa_lote={query}&leilao_pesquisa=&tipo_exibicao=grid&paginacao=0&total_paginas=1&somente_pesquisa=0&e_categoria=1&e_leilao=1&e_subcategoria=0&e_marca=0&e_modelo=0&e_ano=0&e_situacao=0&e_local=0&e_grupo=0"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,de;q=0.8,pt-BR;q=0.7,pt;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "_ga=GA1.1.1775081235.1721184961; __goc_session__=lgtxztildbsejasadykrekuopkwnmhwp; PHPSESSID=b2utklkplauluko1j4d8beccf3; _ga_2LQ3Q2WD1F=GS1.1.1731346152.7.0.1731346183.29.0.0",
        "encoding": "iso-8859-1",
        "origin": "https://www.palaciodosleiloes.com.br",
        "priority": "u=1, i",
        "referer": "https://www.palaciodosleiloes.com.br/site/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    response = requests.post(url, data=payload, headers=headers, params=querystring)
    lotes_html = response.text  # HTML da resposta
    # print(lotes_html)


    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless
    driver = webdriver.Chrome(options=chrome_options)


    driver.get("data:text/html;charset=utf-8," + lotes_html)

    # Encontra os elementos de lote e extrai informações
    lotes = driver.find_elements(By.CSS_SELECTOR, "div.col-md-3")
    resultados = []


    resultados = []
    for lote in lotes:

        modelo_completo = lote.find_element(By.CSS_SELECTOR, ".quebraln").text
        marca = modelo_completo.split(" ")[0]
        modelo = " ".join(modelo_completo.split(" ")[1:])
        resultado = {
            "lote": lote.find_element(By.XPATH, ".//div[contains(text(), 'Lote')]/div").text,
            "marca": marca,
            "modelo": modelo,
            "monta": lote.find_element(By.CSS_SELECTOR, ".mt-0.small").text,
            "ano": lote.find_element(By.CSS_SELECTOR, ".my-0.h6.mb-2").text,
            "thumb": f"https://www.palaciodosleiloes.com.br/site/{lote.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')}",
            "link": f"https://www.palaciodosleiloes.com.br/site/lotem.php?cl={lote.get_attribute('onclick').split('(')[-1].split(',')[0]}"
        }
        # Adiciona o dicionário à lista de resultados
        resultados.append(resultado)

    # Exibe os resultados
    driver.quit()
    print(resultados)
    # return jsonify(resultados)
    return resultados

