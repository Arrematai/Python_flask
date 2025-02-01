import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup

from src.infra.helpers.MarcaCarros import obter_marcas
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log

class ServiceFreitas:
    url: Text = "https://www.freitasleiloeiro.com.br/Leiloes/PesquisarLotes"
    parametros: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        self.Marcas = obter_marcas()
        self.log = Log("")
        
    def initValue(self):
        self.parametros = {
            "Nome": self.query,
            "Categoria": 1,
            "TipoLoteId": 0,
            "FaixaValor": 0,
            "Condicao": 0,
            "PatioId": 0,
            "AnoModeloMin": 0,
            "AnoModeloMax": 0,
            "ArCondicionado": "false",
            "DirecaoAssistida": "false",
            "ClienteSclId": 0,
            "PageNumber": 1,
            "TopRows": self.size
        }
        self.headers= {
            'accept': "*/*",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            'x-requested-with': "XMLHttpRequest",
            "cookie":"__goc_session__=erbpxynnqzymuzctdhfiwyuaqmxtprkc"
        }
        
    def _getTitle(self, lote):
        title = lote.find("div", class_="cardLote-descVeic")
        return title.get_text(strip=True) if title else None
    
    def _getMonta(self, lote: BeautifulSoup):
        card = lote.find("div", class_="cardLote-details")
        monta = card.find('span')
        return getMonta(monta.get_text(strip=True))
    
    def _getModelo(self, title):
        modelo_match = re.match(r"^(\w+)/([\w\s\.\-]+)", title)
        return modelo_match.group(2).split(",")[0] if modelo_match else None
        
    def _getMarca(self, title):
        marca_match = re.match(r"^(\w+)/([\w\s\.\-]+)", title)
        return marca_match.group(1) if marca_match else None
    
    def _getAno(self, title):
        ano_match = re.search(r"(\d{2}/\d{2})", title)
        return ano_match.group(1) if ano_match else None
    
    def _getThumb(self, lote):
        img_tag = lote.find("img", class_="cardLote-img")
        return img_tag["src"] if img_tag else None
    
    def _getLink(self, lote):
        link_tag = lote.find("a", href=True)
        return "https://www.freitasleiloeiro.com.br" + link_tag["href"] if link_tag else None
    
    def _getLoteNumero(self, link):
        return re.search(r"loteNumero=(\d+)", link).group(1) if link else None

        
    def _getLanceInicial(self, page_lote):
        try: 
            page_soup = BeautifulSoup(page_lote.text, "html.parser")
            lance_inicial = page_soup.find("div", class_="fw-bold text-warning")
            lance_inicial_text = lance_inicial.get_text(strip=True)
            return float(lance_inicial_text.replace("R$", "").replace(".", "").replace(",", "."))  if lance_inicial_text  else None 
        except Exception as e:
            return None
    
    def _getValorAtual(self, page_lote):
        try: 
            valor_atual = page_lote.find("div", class_="cardLote-vlr")
            valor_atual = valor_atual.get_text(strip=True)
            return float(valor_atual.replace("R$", "").replace(".", "").replace(",", "."))  if valor_atual  else None
        except Exception as e:
            return None
    
    def exec(self):
        resultados = []

        response = requests.get(self.url, params=self.parametros, headers=self.headers, verify=False)

        if response.status_code != 200:
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            print(f"Erro ao acessar o site na página: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        lotes = soup.find_all("div", class_="cardlote") # Pega cada CARD
    
        for lote in lotes:
            monta = self._getMonta(lote)
            title = self._getTitle(lote)
            marca = self._getMarca(title)
            modelo = self._getModelo(title)
            ano = self._getAno(title)
            thumb = self._getThumb(lote)
            link = self._getLink(lote)
            lote_numero = self._getLoteNumero(link)
            valor_atual = self._getValorAtual(lote)
            
            # # Se nao tem marca nem modelo
            if not marca and not modelo or (not modelo):
                continue
            
            # Se tem Marca
            existeMarca = next((m for m in self.Marcas if m["nome"].lower() in marca.lower()), None)
            
            if existeMarca:
                marca = existeMarca["nome"].capitalize()
            
        
            if not existeMarca:
                existeInModelo = next((m for m in self.Marcas if m["nome"].lower() in modelo.lower()), None)
                marca = existeInModelo["nome"].capitalize()
                
                
            print(marca, modelo)
            
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
                "leiloeiro":"Freitas Leiloeiro",
                "ativo": 1,
            }
        

            resultados.append(resultado)
            

        # Imprimindo os resultados em formato JSON
        # print(json.dumps(resultados, indent=2, ensure_ascii=False))
        return resultados




