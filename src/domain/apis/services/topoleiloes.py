import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup
import urllib3

from src.infra.helpers.Monta import getMonta
from src.infra.helpers.MarcaCarros import obter_marcas

# Desativando avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ServiceTopo:
    url: Text = "https://topoleiloes.com.br/busca"
    parametros: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.Marcas = obter_marcas()
        self.initValue()
        
    def initValue(self):
        self.parametros = {
            "search": self.query,
            "page": 1,
        }
        self.headers= {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            'x-requested-with': "XMLHttpRequest",
            "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
        }
        
    
    def _getModelo(self, lote:BeautifulSoup):
      title = lote.find("a", class_="block")      
      match = re.search(r"(LOTE \d+) - (.+?) - (\d{4}/\d{4})", title.text)
      
      if match:
        return match.group(2).strip()
      else:
        match = re.search(r"LOTE \d+ - (?:[\w/]+) ([\w\s\-]+?) - \d{2,4}/\d{2,4}", title.text)    
        
        if match:
          return match.group(1).strip() if match else None
        else:
          match = re.search(r"- (?:[^/]+/)?([\w\s\-]+) - \d{2,4}/\d{2,4}", title.text)  
          return  match.group(1).strip() if match else None
           

        
    def _getMarca(self, lote:BeautifulSoup):
      title = lote.find("a", class_="block")      
      existeMarca = next((m for m in self.Marcas if m["nome"].lower() in title.text.lower()), None)
      
      if existeMarca:
        return existeMarca["nome"]
      else:
          subTitle = lote.find("p", class_="text-zinc-400")
          existeMarca = next((m for m in self.Marcas if m["nome"].lower() in subTitle.text.lower()), None)
          
          return existeMarca["nome"] if existeMarca else None
        

      
      # return marca.text if marca else None
    
    def _getAno(self, lote:BeautifulSoup):
      title = lote.find("a", class_="block") 
      ano_match = re.search(r"(\d{4}/\d{4})", title.text)
      return ano_match.group(1) if ano_match else None
    
    def _getThumb(self, lote:BeautifulSoup):
        img_tag = lote.find("img")
        return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote:BeautifulSoup):
        title = lote.find("a", class_="block")
        return title["href"] if title else None
    
    def _getLoteNumero(self, lote:BeautifulSoup):
      title = lote.find("a", class_="block")
      match = re.search(r"(\d+)", title.text)
      if match:
        return match.group(1)
    
  
    def exec(self):
        run = True
        resultados = []

        while run:
          
          response = requests.get(self.url, params=self.parametros, headers=self.headers)
          
          if response.status_code != 200:
              self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
              print(f"Erro ao acessar o site na página: {response.status_code}")
              return []
          
          soup = BeautifulSoup(response.text, "html.parser")
          
          lotes = soup.find_all("div", class_="group") # Pega cada CARD
          
          if not lotes or len(lotes) == 0:
            run = False
            continue
          
          
          for lote in lotes:
              modelo = self._getModelo(lote)
              
              if modelo:
                
                marca = self._getMarca(lote)
                ano = self._getAno(lote)
                thumb = self._getThumb(lote)
                link = self._getLink(lote)
                lote = self._getLoteNumero(lote)
                resultado = {
                  "uuid": str(uuid.uuid4()),
                  "lote": lote,
                  "chassi": None,
                  "valor_fipe": None,
                  "valor_atual": None,
                  "tipo_veiculo": None,
                  "marca": marca,
                  "modelo": modelo,
                  "monta": getMonta(""),
                  "ano": ano,
                  "thumb": thumb,
                  "link": link,
                  "leiloeiro":"Topo Leilões",
                  "ativo": 1,
                }
                resultados.append(resultado)
          
              else:
                continue
            
            

          self.parametros["page"] = self.parametros["page"] + 1
            

        # # Imprimindo os resultados em formato JSON
        # # print(json.dumps(resultados, indent=2, ensure_ascii=False))
        return resultados




