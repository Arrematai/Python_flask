import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup

class ServiceVip:
    url: Text = "https://www.vipleiloes.com.br"
    parametros: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        
    def initValue(self):
        self.parametros = {
            "PalavraChave": self.query,
            "Pagina": 1,
        }
        self.headers= {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            'x-requested-with': "XMLHttpRequest",
            "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
        }
        
    
    def _getModelo(self, lote:BeautifulSoup):
        modelo = lote.find("h4", class_="itm-name")
        span = modelo.find('span')
        if span:
          span.extract() 
        return modelo.get_text(strip=True) if modelo else None
        
    def _getMarca(self, lote:BeautifulSoup):
        marca = lote.find("span", class_="itm-marca")
        return marca.text if marca else None
    
    def _getAno(self, title):
        ano_match = re.search(r"(\d{4}/\d{4})", title)
        return ano_match.group(1) if ano_match else None
    
    def _getThumb(self, lote:BeautifulSoup):
        img_tag = lote.find("img", class_="item-imgsrc")
        return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote:BeautifulSoup):
        link_tag = lote.find("a", class_="itm-cdlink", href=True)
        return self.url + link_tag["href"] if link_tag else None
    
    def _getLoteNumero(self, lote:BeautifulSoup):
      lote_num = lote.find("p", class_="itm-info")
      span = lote_num.find('span')
      if span:
        span.extract() 
      return lote_num.get_text(strip=True) if lote_num else None
      
    def _getLanceInicial(self, lote:BeautifulSoup):
        try: 
            lance_inicial = lote.find("p", class_="itm-start")
            span = lance_inicial.find('span')
            if span:
              span.extract() 
            lance_inicial_text = lance_inicial.get_text(strip=True)
            return float(lance_inicial_text.replace("R$", "").replace(".", "").replace(",", "."))  if lance_inicial_text  else None 
        except Exception as e:
            return None
    
    
    def exec(self):
        run = True
        resultados = []

        while run:
          
          response = requests.get(self.url + "/Veiculos/ListarVeiculos", params=self.parametros, headers=self.headers, verify=False)

          if response.status_code != 200:
              print(f"Erro ao acessar o site na página: {response.status_code}")
              return []

          soup = BeautifulSoup(response.text, "html.parser")
          
          listCars = soup.find("div", class_="tav") # Pega cada CARD
          
          lotes = listCars.find_all("div", class_="itm-card") # Pega cada CARD
          
          if not lotes or len(lotes) == 0:
            run = False
            continue;
          
          
          for lote in lotes:
            monta = "Não Informada"
            marca = self._getMarca(lote)
            modelo = self._getModelo(lote)
            ano = self._getAno(modelo)
            thumb = self._getThumb(lote)
            link = self._getLink(lote)
            valor_atual = self._getLanceInicial(lote)
            lote_numero = self._getLoteNumero(lote)
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": lote_numero,
                "chassi": None,
                "valor_fipe": None,
                "valor_atual": valor_atual,
                "tipo_veiculo": None,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "ano": ano,
                "thumb": thumb,
                "link": link,
                "leiloeiro":"Vip Leilões",
                "ativo": 1,
            }
            resultados.append(resultado)
          
          self.parametros["Pagina"] = self.parametros["Pagina"] + 1
            

        # # Imprimindo os resultados em formato JSON
        # # print(json.dumps(resultados, indent=2, ensure_ascii=False))
        return resultados




