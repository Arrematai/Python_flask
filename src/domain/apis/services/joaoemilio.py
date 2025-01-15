import requests
import re  # Para expressões regulares
from typing import Text
import uuid


class ServiceJoaoEmilio:
    url: Text = "https://www.joaoemilio.com.br"
    params: Text
    headers: Text
    
    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        
    def initValue(self):
        self.params = {}
        self.url = f'{self.url}/lotes/search?search={self.query}'
        self.headers = {
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

    def _getLote(self, html):
        lote_match = re.search(r'<h4>Lote (\d+)</h4>', html)
        return lote_match.group(1) if lote_match else "N/A"
    
    def _getTitle(self, html):
        marca_modelo_match = re.search(r'<h5>(.*?)</h5>', html)
        descricao = marca_modelo_match.group(1) if marca_modelo_match else "N/A"
        return descricao.split("/", 1)
    
    def _getAno(self, html):
        ano_modelo_match = re.search(r'<b>Ano/Modelo:</b>\s*\d{4}/(\d{4})', html)
        return ano_modelo_match.group(1) if ano_modelo_match else "N/A"
    
    def _getThumb(self, html):
        thumb_match = re.search(r"background:\s*url\('([^']+)'\)", html)
        return thumb_match.group(1) if thumb_match else "N/A"
        
    def _getLink(self, html):
        link_match = re.search(r'<a href="(https://www\.joaoemilio\.com\.br/item/\d+/detalhes\?page=\d+)"', html)
        return link_match.group(1) if link_match else "N/A"
    
    def _getValorAtual(self, html):
        try:
            valor_inicial = re.search(r'<h4 class="mb-0">R\$\s?([\d.,]+)</h4>', html)
            return float(valor_inicial.group(1).replace("R$", "").replace(".", "").replace(",", ".")) if valor_inicial.group(1) else "N/A"
        except Exception as e:
            return None

    def exec(self):

        response = requests.request("GET", self.url, headers=self.headers, params=self.params)

        html_content = response.text

        # Extraindo dados com expressões regulares ou buscas de string
        lotes = re.findall(r'<div class="lote ">.*?</div> <!-- ./card -->', html_content, re.DOTALL)

        resultados = []
        for html in lotes:
            lote = self._getLote(html)
            title = self._getTitle(html)
            marca = title[0] if len(title) > 0 else "N/A"
            modelo = title[1] if len(title) > 1 else "N/A"
            ano = self._getAno(html)
            thumb = self._getThumb(html)
            link = self._getLink(html)
            valor_atual = self._getValorAtual(html)
            
        
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": lote,
                "chassi": None,
                "valor_fipe": None,
                "valor_atual": valor_atual,
                "tipo_veiculo": None,
                "marca": marca,
                "modelo": modelo,
                "monta": "Pequena Monta",  # Exemplo de valor padrão
                "ano": ano,
                "thumb": thumb,
                "link": link,
                "leiloeiro":"João Emilio",
                "ativo": 1,
            }
            resultados.append(resultado)
        
        return resultados



