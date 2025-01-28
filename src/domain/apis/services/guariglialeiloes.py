import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup

from src.helpers.MarcaCarros import obter_marcas
from src.helpers.Monta import getMonta
from src.infra.service.Logging import Log

class ServiceGuariglia:
    url: Text = "https://www.guariglialeiloes.com.br"
    parametros: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        self.Marcas = obter_marcas()
        self.log = Log("")
        
    def initValue(self):
        self.url = f'{self.url}/lotes/search?search={self.query}' 
        self.headers= {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            'x-requested-with': "XMLHttpRequest",
            "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
        }
        
    def _getMarcaModelo(self, lote: BeautifulSoup):
        marca_modelo_element = lote.find('b', text='Marca/Modelo:')
        if marca_modelo_element:
          marca_modelo = marca_modelo_element.next_sibling.strip()
          return marca_modelo
        else:
          return ""
        
    def _getMarca(self, marca_modelo: str):
        marca_match = re.match(r"^(\w+)/([\w\s\.\-]+)", marca_modelo)
        return marca_match.group(1) if marca_match else None
      
    def _getModelo(self, marca_modelo: str):
        modelo_match = re.match(r"^(\w+)/([\w\s\.\-]+)", marca_modelo)
        return modelo_match.group(2) if modelo_match else None
    
    def _getAno(self, lote: BeautifulSoup):
        ano_element = lote.find('b', text='Ano/Modelo:')
        if ano_element:
          return ano_element.next_sibling.strip()
        else:
          return ""
    
    def _getThumb(self, lote: BeautifulSoup):
        img_tag = lote.find("img", class_="img-fluid")
        return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote: BeautifulSoup):
        link_tag = lote.find("a", href=True)
        return link_tag["href"] if link_tag else None
    
    def _getLoteNumero(self, lote: BeautifulSoup):
        lote_tag = lote.find("h5", class_="numero-lote")        
        return re.search(r"Lote (\d+)", lote_tag.text).group(1) if lote_tag else None

        
    def _getLanceInicial(self, page_lote: BeautifulSoup):
        try: 
            lance_inicial = page_lote.find("div", class_="lance")
            lance_inicial_text = lance_inicial.get_text(strip=True)
            return float(lance_inicial_text.replace("R$", "").replace(".", "").replace(",", "."))  if lance_inicial_text  else None 
        except Exception as e:
            return None
    
    def exec(self):
        resultados = []

        response = requests.get(self.url, headers=self.headers, verify=False)

        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            print(f"Erro ao acessar o site na página: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        lotes = soup.find_all("div", class_="lote") # Pega cada CARD
        
    
        for lote in lotes:
          body = lote.find("div", class_="body-lote")
          
          monta = "Não informada"
          marca_modelo = self._getMarcaModelo(body)
          marca = self._getMarca(marca_modelo)
          modelo = self._getModelo(marca_modelo)
          ano = self._getAno(body)
          link = self._getLink(body)
          thumb = self._getThumb(lote)
          lote_numero = self._getLoteNumero(body)
          valor_atual = self._getLanceInicial(lote)
          
        
        
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
              "leiloeiro":"Guariglia Leilões",
              "ativo": 1,
          }
        

          resultados.append(resultado)
            

        # Imprimindo os resultados em formato JSON
        # print(json.dumps(resultados, indent=2, ensure_ascii=False))
        return resultados




