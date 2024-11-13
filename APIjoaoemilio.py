import requests
import re
import json




def Joao_Emilio (query):

    url = "https://www.joaoemilio.com.br/lotes/search"

    querystring = {"search":f"{query}"}

    payload = ""
    headers = {
        "cookie": "modal-8137c1fdeba6872580fff3801a7a1e55=1; _hjSession_3327924=eyJpZCI6IjkyZWJlMWJmLWI3YTUtNGFmOS1hOGJjLTc5ZDg2NWJjYmYzYyIsImMiOjE3MzE0MzM1MzIxOTMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; cf_clearance=VmV90m6JNFDi0RaeFMqV_kdUhU1T8ITaR5DEoEjmv3I-1731433532-1.2.1.1-VXe4y9ZWz5uHUCvKqaM7wx4SXtqC2faqMrbNrP6ZK63deFSzsL1WNb2vDw1QpVbEZOMGYhDT0Xb7FlmD8qd3UhLfXjlO5AwOVzCP8eegFPsOuSYa4ErGiW9fhffTgg0STOEJ1XwZjJFc8qwH1VjTHGHYWcwvP0ACTbpCxQzfgh5gj_yiPVPaMQwyLkJYNgSSx6iDjfEfnWWSoAzJhWMNmPoxfKMcwi6qehMUnkqPgUniIEbs.621uTRixBsj5IVx5rVwSknuGQFgyReK2zZCV8q.cg2EU.kJRrNXAq6pF4YrSzFH6H7bNy_65.8cNNkz1q7AIdUwJnPKUcg0Ob_SSGHnovM0CniRy1Gchhp0S69Q0roXhsuPebkRw_K0NFMSuFqWgjHqL55sa8rv5449yQ; _gcl_au=1.1.262518452.1731433532; _gid=GA1.3.571009262.1731433532; twk_idm_key=yAG_g0a_dB-nNpoQGtEua; _hjSessionUser_3327924=eyJpZCI6ImQ2MjVhOGEyLWQ1MzEtNWVhYS05M2I2LWI4MTk1NDllODM2ZSIsImNyZWF0ZWQiOjE3MzE0MzM1MzIxOTIsImV4aXN0aW5nIjp0cnVlfQ==; laravel_session=eyJpdiI6IkdnWm9NRTdlRVZQYUdVQ3hKU1VmTVE9PSIsInZhbHVlIjoicW4rR1dZMDREd0lhcDhJVGJmSGJEdWlicUcrNTdRV09rMjV1VVhMWmZORTRTXC9yWGFlcGEzZjVZM3BWbnkzdDBJUTdRMlJOMmhJZnVUT3VLUmhoTjRnPT0iLCJtYWMiOiI4ZDNlNGVkMWRiYTA3ZjI1MWE1ODA1YzEwZWI0OWE4NWQ2ZjgzOGM0NWFiZjk0M2FiYTY3NmI3YjU5MzE0MWQxIn0%3D; _ga_X334VRVJ87=GS1.1.1731433532.1.1.1731433603.0.0.0; _ga=GA1.3.521269643.1731433532; _gat_gtag_UA_61727303_1=1; TawkConnectionTime=0; _ga_T4ZP574MMC=GS1.1.1731433532.1.1.1731433628.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.joaoemilio.com.br/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }


    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    html_content = response.text

    # Extraindo dados com expressões regulares ou buscas de string
    lotes = re.findall(r'<div class="lote ">.*?</div> <!-- ./card -->', html_content, re.DOTALL)

    resultados = []
    for lote_html in lotes:
        lote_match = re.search(r'<h4>Lote (\d+)</h4>', lote_html)
        lote = lote_match.group(1) if lote_match else "N/A"

        marca_modelo_match = re.search(r'<h5>(.*?)</h5>', lote_html)
        descricao = marca_modelo_match.group(1) if marca_modelo_match else "N/A"
        descricao_parts = descricao.split("/", 1)
        marca = descricao_parts[0] if len(descricao_parts) > 0 else "N/A"
        modelo = descricao_parts[1].split(" ")[0] if len(descricao_parts) > 1 else "N/A"

        ano_modelo_match = re.search(r'<b>Ano/Modelo:</b>\s*\d{4}/(\d{4})', lote_html)
        ano_modelo = ano_modelo_match.group(1) if ano_modelo_match else "N/A"

        thumb_match = re.search(r"background:\s*url\('([^']+)'\)", lote_html)
        thumb = thumb_match.group(1) if thumb_match else "N/A"

        link_match = re.search(r'<a href="(https://www\.joaoemilio\.com\.br/item/\d+/detalhes\?page=\d+)"', lote_html)
        link = link_match.group(1) if link_match else "N/A"

        resultado = {
            "lote": lote,
            "marca": marca,
            "modelo": modelo,
            "monta": "Pequena Monta",  # Exemplo de valor padrão
            "ano": ano_modelo if ano_modelo else "N/A",
            "thumb": thumb,
            "link": link if link else "N/A"
        }
        resultados.append(resultado)
    print(resultados)
    print(html_content)
    return resultados



