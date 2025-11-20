import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup
import cloudscraper

from src.infra.helpers.Monta import getMonta
from src.infra.helpers.MarcaCarros import marcaIsExiste,replace_marcas
from src.infra.service.Logging import Log


class ServiceMilan:
    url: Text = "https://milanleiloes.com.br/Busca/Busca.asp"
    parametros: Text
    headers: Text
    pagina: Text

    def __init__(self, query, size, api):
        self.query = query
        self.size = size
        self.api = api
        self.resultados = []
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.parametros = {
          "btnProcurar": "0",
          "selOpcaoTodas": "Procurar",
          "txtBusca": self.query,
        }
        self.headers= {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            'x-requested-with': "XMLHttpRequest",
            "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
        }
        
    
    def _getModelo(self, carro):
      match = re.search(r'(?i)(\b\w+\b)\s+(.+?)\s+(\d+\.\d+)\s+\w+\s+\d+', carro)

      if match:
        return match.group(2) + " " + match.group(3) if match else None
      else:
        match = re.search(r'(?i)(\b\w+\b)\s+(.+?)\s+\w+\s+\d+', carro)
        return match.group(2) if match else None
        
    def _getMarca(self, title):
      match = re.search(r'\b(\w+)\s+(\w+)\s+', title)  # Captura a primeira palavra como marca
      return replace_marcas(match.group(1)) if match else None

    
    def _getAno(self, title):
      regex = r'\bANO\s\d{4}/\d{4}\b'
      match = re.search(regex, title)
      return match.group(0).replace("ANO","") if match else None
    
    # def _getThumb(self, lote:BeautifulSoup):
    #   img_tag = lote.find("img")
    #   return img_tag["src"] if img_tag else None
    
    def _getLink(self, html_content):
      pattern = r"javascript:AbrirLances2\((\d+),\s*'(\d+)'"
      match = re.search(pattern, str(html_content))

      if match:
        parametro1 = match.group(1)  # Primeiro parâmetro (14007)
        parametro2 = match.group(2)  # Segundo parâmetro ('087')
        return f'https://milanleiloes.com.br/Leiloes/Lance/lote.asp?CL={parametro1}#Lote={parametro2}'
      else:
        return None
    
      
    
    def exec(self):

        # response = requests.post(self.url, params=self.parametros, headers=self.headers)

        scraper = cloudscraper.create_scraper()
        response = scraper.get("https://api.scrapfly.io/scrape?tags=player%2Cproject%3Adefault&key=scp-live-0f1c0f0c671e457788540b8d2f1636e5&url=https%3A%2F%2Fmilanleiloes.com.br%2FBusca%2FBusca.asp")


        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": self.resultados, "http_code": response.status_code }
        
        
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        table = []

        print(tables)


        if tables and len(tables) > 2:
            table = tables[2]


        if not table or len(table) <= 0:
           return []

        lotes = table.find_all("tr")
        lotes = lotes[1:]

                  
        for lote in lotes:
          valores = lote.find_all("td")
          lote_numero = valores[0]
          title = valores[1]
          url = valores[2]
          monta = getMonta("")
          marca = self._getMarca(title.text)
          modelo = self._getModelo(title.text)
          ano = self._getAno(title.text)
          thumb = None
          link = self._getLink(url)
          
          resultado = {
              "uuid": str(uuid.uuid4()),
              "lote": lote_numero.text,
              "chassi": None,
              "valor_fipe": None,
              "valor_atual": None,
              "tipo_veiculo": None,
              "marca": marca,
              "modelo": modelo,
              "monta": monta,
              "ano": ano,
              "thumb": thumb,
              "link": link,
              "leiloeiro":"Milan Leilões",
              "ativo": 1,
          }

          self.resultados.append(resultado)
      
            

        return { "resultados": self.resultados, "http_code": response.status_code }




