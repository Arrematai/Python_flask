import requests
import re  # Para expressões regulares
from src.helpers.Monta import getMonta
from typing import Text
import uuid

class ServiceSuperBid:
    url: Text = "https://api.sbwebservices.net/offer-query/seo/offers"
    payload: Text
    params: Text
    headers: Text
    
    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        
    def initValue(self):
        self.params = {
        "keyword": self.query,
        "locale": "pt_BR",
        "orderBy": "score:desc",
        "pageNumber": "1",
        "pageSize": self.size,
        "portalId": "[2,15]",
        "requestOrigin": "marketplace",
        "searchType": "opened",
        "timeZoneId": "America/Sao_Paulo",
        "urlSeo": "https://www.superbid.net/busca/"
        }
        self.payload = {}
        self.headers = {
            "accept": "application/json",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "ApiKey d2NHYVRKRUI0R0s5Q2kwRXNfNGU6b0xGVDl3blFRd0t6S2hZVURKZThHZw==",
            "content-type": "application/json",
            "origin": "https://www.sodresantoro.com.br",
            "priority": "u=1, i",
            "referer": "https://www.sodresantoro.com.br/",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
        }

    def _getAno(self,title):
        ano_match = re.search(r"\b((19|20)?[0-9]{2}(/(19|20)?[0-9]{2})?)\b", title)
        return ano_match.group(0) if ano_match else None

    
    def _getMarca(self, title, marcas):
        marca_info = next((m for m in marcas if m['nome'].lower() in title.lower()), None)
        if marca_info:
            return marca_info['nome']
        else:
            return None

    def exec(self):
        response = requests.request("GET", self.url, data=self.payload, headers=self.headers, params=self.params)

        data = response.json()

        resultados = []

        for item in data['offers']:
        
            valor_atual = item["price"] if item["price"] else None
            
            template = item['product'].get('template', None)

            ano = None
            marca = None
            modelo = None
                     
            if template and len(template['groups']) > 0:
                propriedades = template['groups'][0]['properties']
                if propriedades:
                    for property in propriedades:
                        if property['id'] == 'anofabricacao':
                            ano = property['value']
                        if property['id'] == 'marca':
                            marca = property['value']
                        if property['id'] == 'modelo':
                            modelo = property['value']
                        


            descricao = item['product'].get('shortDesc', 'Descrição não disponível')
            
            monta = getMonta(descricao.lower())

            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": item['lotNumber'],
                "chassi": None,
                "valor_fipe": None,
                "valor_atual": valor_atual,
                "tipo_veiculo": None,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "ano": ano,
                "thumb": item['product'].get('thumbnailUrl', 'Imagem não disponível'),
                "link": f"https://www.superbid.net/oferta/{item['id']}",
                "leiloeiro": "SuperBid",
                "ativo": 1,
            }

            if marca and modelo and ano:
                resultados.append(resultado)

        return resultados


