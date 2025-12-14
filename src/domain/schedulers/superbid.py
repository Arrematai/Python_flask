from datetime import datetime, timedelta
import math
import requests
import re  # Para expressões regulares
from typing import Text
import uuid


from src.domain.lotes.repository import LotesRepository
from src.domain.schedulers.sincronizar import sincronizar
from src.domain.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.infra.helpers.MarcaCarros import obter_marcas, replace_marcas
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log

# https://offer-query.superbid.net/seo/offers/?filter=&keyword=bmw&locale=pt_BR&orderBy=score:desc&pageNumber=1&pageSize=99999&portalId=[2,15]&requestOrigin=marketplace&searchType=opened&timeZoneId=America/Sao_Paulo&urlSeo=https://www.superbid.net/busca/bmw&requestOrigin=marketplace

class SchedulerSuperBid:
    url: Text
    payload: Text
    params: Text
    headers: Text
    
    def __init__(self, scheduler: str, schedulerLogRepository: SchedulersLogRepository, lotesRepository: LotesRepository):
        self.scheduler = scheduler
        self.schedulerLogRepository = schedulerLogRepository
        self.lotesRepository = lotesRepository
        self.size = 1
        self.page = 1
        self.url = f"https://offer-query.superbid.net/seo/offers/?filter=&locale=pt_BR&orderBy=score:desc&pageNumber={self.page}&pageSize={self.size}&portalId=[2,15]&preOrderBy=orderByFirstOpenedOffersAndSecondHasPhoto&requestOrigin=marketplace&searchType=opened&timeZoneId=America/Sao_Paulo&urlSeo=https://www.superbid.net/categorias/carros-motos&requestOrigin=marketplace"
        self.resultados = []
        self.initValue()
        self.log = Log("")
        self.Marcas = obter_marcas()
        
    def initValue(self):
        # self.params = {
        #     # "keyword": self.query,
        #     "filter": "",
        #     "locale": "pt_BR",
        #     "orderBy": "score:desc",
        #     "pageNumber": "1",
        #     "pageSize": self.size,
        #     "portalId": "[2,15]",
        #     "requestOrigin": "marketplace",
        #     "searchType": "opened",
        #     "timeZoneId": "America/Sao_Paulo",
        #     "urlSeo": "https://www.superbid.net/busca/",
        #     "filter": "auction.modalityDesc:leilao",
        #     "timeZoneId": "America/Sao_Paulo"
        # }
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
        

        
    def _handleAno(self, descricao):
        ano_match = re.search(r"\b((19|20)?[0-9]{4}(/(19|20)?[0-9]{4})?)\b", descricao)
        
        if ano_match: 
            return ano_match.group(0) if ano_match else None
        
        return None
        
    def _handleMarca(self, descricao):
        padrao = re.compile(r'''
                (?ix)                        # i = ignore case, x = verbose
                ^\s*
                (?:DIREITOS?\s+AQUISITIV(?:OS|O)\s*[-:]\s*)?   # <<< IGNORA DIREITOS AQUISITIVOS
                (?:LOTE[: ]*\d*[:]?\s*)?     # Lote 15:
                (?:DESMONTE:|PRENSA:)?\s*    # DESMONTE: / PRENSA:
                (?:IMP\.)?\s*                # IMP.
                (?:VE[IÍ]CULO|AUTOM[ÓO]VEL|QUADRICICLO|CAMINHONETE|CAMINH[ÃA]O|MOTO|MOTOCICLETA|PICK[- ]?UP|SUV|VAN)?\s*  # tipo de veículo
                (?:MARCA[: ]*)?\s*           # MARCA ou MARCA:
                (?:I/|I:|I\s+)?\s*           # "I/", "I:", E "I⎵"
                (?:(?:JTA|JTZ)\b\s*)*        # ignora JTA / JTZ
                ([A-ZÁ-Ú][A-ZÁ-Ú0-9]+)       # <-- AQUI é a MARCA REAL
                ''', re.VERBOSE | re.IGNORECASE)
        match = padrao.search(descricao)
        
        if not match:
            return None

        marca = match.group(1)
        
        return marca
    
    def _handleModelo(self, descricao):
        regex = re.compile(r'''
(?ix)
(?:
    ^\s*(?:VE[IÍ]CULO\s*)?FIAT\s+(147|500)\b

|

    MODELO:\s*([A-Z0-9 .\-_/]+)

|

    modelos?\s*[:\-]?\s*([A-Z0-9 .\-_/]+?)(?=,|\s+cor|\s+ano|\s+placa|\s+RENAVAM|\s+DOAD|$)

|

    [A-Z0-9Á-Ú\-]+/\s*([A-Z0-9 .\-_/]+)

|

    (?:AUTOM[ÓO]VEL|VE[IÍ]CULO|CAMINHONETE|QUADRICICLO|CAMINH[ÃA]O|MOTO|MOTOCICLETA|PICK[- ]?UP|SUV|VAN)?\s*
    [A-ZÁ-Ú][A-ZÁ-Ú0-9]+\s+
    (
        (?!\d{4}\b)                   # NÃO PODE começar com ano
        (?:[A-Z0-9 .\-_/](?!\d{4}\b))+ # NÃO PODE conter ano no meio
        (?<!\b\d{4})                  # NÃO PODE terminar com ano
    )
    (?= ,?\s*\d{4}(?:/\d{4})?\b )
)
''', re.VERBOSE | re.IGNORECASE)
        m = regex.search(descricao)
        if m:
            grupo = next((g for g in m.groups() if g), None)
            if grupo:
                return re.sub(r'\s{2,}', ' ', grupo.strip())
        
        return None

      
    def exec(self):
      print("INICIADO SCHEDULER SUPERBID", datetime.now());
      response = requests.request("GET", self.url, headers=self.headers)
      
      print("Status Code:", response.status_code)
     
      if response.status_code != 200:
          self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
          return { "resultados": self.resultados, "http_code": response.status_code }

      data = response.json()
      
      total_itens = data.get("total", 0)
      paginas = math.ceil(total_itens / 1000)
      
      for pagina in range(1, paginas + 1):
        self.page = pagina
        self.size = 1000
        self.url = f"https://offer-query.superbid.net/seo/offers/?filter=&locale=pt_BR&orderBy=score:desc&pageNumber={self.page}&pageSize={self.size}&portalId=[2,15]&preOrderBy=orderByFirstOpenedOffersAndSecondHasPhoto&requestOrigin=marketplace&searchType=opened&timeZoneId=America/Sao_Paulo&urlSeo=https://www.superbid.net/categorias/carros-motos&requestOrigin=marketplace"
        
        response = requests.request("GET", self.url, headers=self.headers)
        print(f"Processando página {self.page} de {paginas} - Status Code:", response.status_code)
        
        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": self.resultados, "http_code": response.status_code }
        
        data_page = response.json()
    
        print(len(data_page.get('offers', [])))
    
    
        lotes = data_page['offers'] if 'offers' in data_page else []
        
        for item in lotes:
            tiposAceitos = ["Caminhões", "Ônibus", "Carros","Motos", "Vans"]
            
            tipo_veiculo = item["product"]["subCategory"]["category"].get("description")
            
            if tipo_veiculo not in tiposAceitos:
                continue
            
            descricao = item['product'].get('shortDesc', None)
            
            
            ignorar_texto = ["lote exclusivo para desmonte", "lote exclusivo para prensa", "lote exclusivo para reciclagem", "sucata", "peças", "lote exclusivo para peças", "sucatas"]
            if any(ignorar in descricao.lower() for ignorar in ignorar_texto):
                continue
            
            
            try:
              valor_atual = item["price"] if item["price"] not in ("", None) else None
            except:
              valor_atual = None
              
            data_leilao = item.get("auction").get("beginDate")
            cidade = item["product"].get("location").get("city", None)
            estado = item["product"].get("location").get("state", None)
            
            groups = []
            
            try:
                groups = item["product"]["template"]["groups"]
            except:
                continue
            
            valor = {}
            for grupo in groups:
              properties = grupo.get("properties", [])
              
              for prop in properties:
                  chave = prop.get("id")  # ex: "marca", "cor", "motor"
                  valor_prop  = prop.get("value")
                  
                  # Se não existir, adiciona como None
                  if chave:
                      valor[chave] = valor_prop  if valor_prop not in ("", None) else None


            ano = f'{valor.get("anofabricacao")}/{valor.get("anomodelo")}' if valor.get("anomodelo") else valor.get("anofabricacao")
            marca = valor.get("marca")
            modelo = valor.get("madelo")
            combustivel = valor.get("combustivel")
            cor = valor.get("cor")
            transmissao = valor.get("transmissao")
            valor_fipe = valor.get("valortabelafipe")
            thumb = item['product'].get('thumbnailUrl', None)  
            lote = item['lotNumber'] 
            
            
            if ano is None:
                ano = self._handleAno(descricao)
                
            if marca is None:
                marca = self._handleMarca(descricao)
                
            if modelo is None:
                modelo = self._handleModelo(descricao)
                
            # print(descricao, "|" , marca, "|" ,modelo, "|" ,ano)
        
            if marca is None or modelo is None:
                continue
            
            # NA API VEM MUITO COISA JUNTO, COMO LIXO OU OUTROS CARROS, assim do quando bate parececido
            resultado = {
                "uuid": str(uuid.uuid4()),
                "descricao": descricao,
                "data_leilao": data_leilao,
                "cidade": cidade,
                "estado": estado,
                "condicao": None,
                "lote": lote,
                "chassi": None,
                "valor_fipe": valor_fipe,
                "valor_atual": valor_atual,
                "tipo_veiculo": tipo_veiculo,
                "marca": marca,
                "modelo": modelo,
                "monta": getMonta(None),
                "ano": ano,
                "placa": None,
                "cor": cor,
                "combustivel": combustivel,
                "kilometragem": None,
                "transmissao": transmissao,
                "thumb": thumb,
                "link": f"https://www.superbid.net/oferta/{item['id']}",
                "leiloeiro": "SuperBid",
                "api":self.scheduler,
                "ativo": 1,
            }
            self.resultados.append(resultado)
              

      dbLotes = self.lotesRepository.getLotesByApi(self.scheduler)
      inserir,atualizar, remover = sincronizar(dbLotes, self.resultados)

      print("Insert: ",len(inserir))
      print("Updates: ",len(atualizar))
      print("Desativados: ", len(remover))
      
      if len(inserir) > 0:
          for lote in inserir:
              self.lotesRepository.insertLote(lote)

      if len(atualizar) > 0:
          for lote in atualizar:
              lote["updated_at"] = datetime.now()
              lote["ativo"] = 1
              self.lotesRepository.updateLote(lote)

      if len(remover) > 0:
          for lote in remover:
              self.lotesRepository.updateLote({
              'id': lote.get("id"),
              'ativo': 0,
              "updated_at": datetime.now(),
              })
      

      self.schedulerLogRepository.insertLog({ 
          "nome": self.scheduler,
          'status': 'success',
          "duration": 0,
          "results": len(self.resultados)
      })
        
      print("FINALIZADO SCHEDULER SUPERBID")
      
      


