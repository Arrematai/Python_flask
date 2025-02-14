from flask import jsonify
import requests
import re  # Para expressões regulares
from typing import Text
import uuid


from src.infra.helpers.MarcaCarros import obter_marcas, replace_marcas
from src.infra.helpers.Monta import getMonta

class ServiceSuperBid:
    url: Text = "https://api.sbwebservices.net/offer-query/seo/offers"
    payload: Text
    params: Text
    headers: Text
    
    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        self.Marcas = obter_marcas()
        
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
            "urlSeo": "https://www.superbid.net/busca/",
            "filter": "auction.modalityDesc:leilao"
        }
        self.headers =  {
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

    def _getAno(self,title):
        ano_match = re.search(r"\b((19|20)?[0-9]{4}(/(19|20)?[0-9]{4})?)\b", title)
        
        if ano_match: 
            return ano_match.group(0)
        else:
            ano_match = re.search(r"\b((19|20)?[0-9]{2}(/(19|20)?[0-9]{2})?)\b", title)
            return ano_match.group(0) if ano_match else None

    
    # def _getMarca(self, marca):
    #     if not marca: 
    #         return None
    #     marca_info = next((m for m in self.Marcas if replace_marcas(m['nome'].lower()) in marca.lower()), None)
    #     if marca_info:
    #         return marca_info['nome']
    #     else:
    #         return None
        
    def _handleAno(self, item):
        ano = None
        template = item['product'].get('template', None)
        if template and len(template['groups']) > 0:
            propriedades = template['groups'][0]['properties']
            if propriedades:
                for property in propriedades:
                    if property['id'] == 'anofabricacao':
                        ano = property['value']
                    if property['id'] == 'anomodelo':
                        ano = ano+"/"+property['value']
        
        if not ano:
            ano = self._getAno(item['product']["shortDesc"])
            
        return ano
    
    def _handleMarca(self, item):
        marca = None 
        template = item['product'].get('template', None)        
        if template and len(template['groups']) > 0:
            propriedades = template['groups'][0]['properties']
            if propriedades:
                for property in propriedades:
                    if property['id'] == 'marca':
                        marca = property['value']
        
        if not marca:
                marca = item['product']["brand"].get("description", None)
        
        return replace_marcas(marca) if marca else None
    
    def _handleModelo(self, item):
        modelo = None
        template = item['product'].get('template', None)
        if template and len(template['groups']) > 0:
            propriedades = template['groups'][0]['properties']
            if propriedades:
                for property in propriedades:
                    if property['id'] == 'modelo':
                        modelo = property['value']
                        
                        
        if not modelo :
            modelo = item['product']["model"].get("description", None)

        return modelo

    def exec(self):
        response = requests.request("GET", self.url, headers=self.headers, params=self.params)

        data = response.json()

        resultados = []
        
        # print(data['offers'][131])
        # exit(0)
        
        
        for item in data['offers']:
            
            # Caminhões & Ônibus Carros & Motos
            type = item["product"]["productType"].get("description")
            
            if type != "Caminhões & Ônibus" and type != "Carros & Motos":
                continue
            
            valor_atual = item["price"] if item["price"] else None



            ano = self._handleAno(item)
            marca = self._handleMarca(item)
            modelo = self._handleModelo(item)
        
                
            ## MONTA               
            descricao = item['product'].get('shortDesc', 'Descrição não disponível')
            monta = getMonta(descricao.lower())

            # SE ATE AGORA NAO CONSEGUI PEGAR NO JSON PEGA NO shortDesc
            if not marca and not modelo:
                split = descricao.split("/")
                if len(split) >= 2:
                    marca = replace_marcas(split[0]) if split[0] else None
                    modelo = split[1]


            # NA API VEM MUITO COISA JUNTO, COMO LIXO OU OUTROS CARROS, assim do quando bate parececido
            if marca and modelo:
                if re.search(r'\b' + re.escape(self.query) + r'\b', marca, re.IGNORECASE) or re.search(r'\b' + re.escape(self.query) + r'\b', modelo, re.IGNORECASE):    
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
                    

                    if marca and modelo:
                        resultados.append(resultado)
                

        return resultados


