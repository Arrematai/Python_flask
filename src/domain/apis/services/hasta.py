import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup


from src.infra.helpers.Monta import getMonta
from src.infra.helpers.MarcaCarros import marcaIsExiste



class ServiceHasta:
    url: Text = "https://www.hastapublica.com.br/busca/"
    parametros: Text
    headers: Text
    pagina: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        self.pagina = 0
        
    def initValue(self):
        self.parametros = {
          "id_categoria": "1",
          "id_sub_categoria": "",
          "localidade": "",
          "data": "",
          "id_leilao": "",
          "palavra": self.query,
        }
        self.headers= {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            'x-requested-with': "XMLHttpRequest",
            "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
        }
        
    
    def _getModelo(self, title,marca):
      regex = rf'{re.escape(marca)}\s+([A-Za-z0-9\s]+),\s*ano/modelo\s*\d{{4}}/\d{{4}}'
      match = re.search(regex, title)
      return match.group(1).strip() if match else None
        
    def _getMarca(self, title:BeautifulSoup):
      match = re.search(r'\b(\w+)\s+(\w+)\s+', title)  # Captura a primeira palavra como marca

      marca = marcaIsExiste(match.group(2)) if match else None

      if marca:
        return marca
      else:
        marca = re.sub(r'\b(Veículo|Direitos do veículo)\b', '', title).strip() # Remove "Direitos do veículo"
        match = re.search(r'\b(\w+)\s+(\w+)\s+', marca)
        return match.group(1) if match else None

    
    def _getAno(self, title):
      regex = r'\bano/modelo\s\d{4}/\d{4}\b'
      match = re.search(regex, title)
      return match.group(0).replace("ano/modelo","") if match else None
    
    def _getThumb(self, lote:BeautifulSoup):
      img_tag = lote.find("img")
      return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote:BeautifulSoup):
      link_tag = lote.find("a", href=True)
      return link_tag["href"] if link_tag else None
    
      
    def _getLanceInicial(self, lote:BeautifulSoup):
        try: 
            lance_inicial = lote.find('dt', text="Lance Inicial").find_next('dd').text.strip()
            return float(lance_inicial.replace("R$", "").replace(".", "").replace(",", "."))  if lance_inicial  else None 
        except Exception as e:
            return None
    
    
    def exec(self):
        run = True
        resultados = []

        while run:
          
          response = requests.get(self.url + str(self.pagina), params=self.parametros, headers=self.headers)

          if response.status_code != 200:
              print(f"Erro ao acessar o site na página: {response.status_code}")
              return []
          
          soup = BeautifulSoup(response.text, "html.parser")
          listCars = soup.find_all("li", class_="card-leilao") # Pega cada CARD

          if not listCars or len(listCars) == 0:
            run = False
            continue;
          
                      
          for lote in listCars:
            monta = getMonta("")
            title = lote.find("dd", class_="titleInsideLote").text
            marca = self._getMarca(title)
            modelo = self._getModelo(title,marca)
            ano = self._getAno(title)
            thumb = self._getThumb(lote)
            link = self._getLink(lote)
            lote_numero = "1"
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": lote_numero,
                "chassi": None,
                "valor_fipe": None,
                "valor_atual": self._getLanceInicial(lote),
                "tipo_veiculo": None,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "ano": ano,
                "thumb": thumb,
                "link": link,
                "leiloeiro":"Hasta Pública",
                "ativo": 1,
            }
            resultados.append(resultado)
          
          self.pagina = self.pagina + 9
            

        # # Imprimindo os resultados em formato JSON
        # # print(json.dumps(resultados, indent=2, ensure_ascii=False))
        return resultados




