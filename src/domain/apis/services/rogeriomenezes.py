import requests
from bs4 import BeautifulSoup, Tag
import re  
from typing import Text
import uuid

from src.helpers.Monta import getMonta
from src.helpers.MarcaCarros import obter_marcas

class ServiceRogerio:
    url: Text = "https://www.rogeriomenezes.com.br/busca"
    payload: Text
    params: Text
    headers: Text
    
    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.Marcas = obter_marcas()
        self.initValue()

    def initValue(self):
        self.params = {"interesse": self.query}

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
    
    def _getTitle(self, resultado: Tag):
        return resultado.select_one("h3").get_text(strip=True)
    
    def _getLink(self, resultado: Tag):
        link_tag = resultado.select_one("a.img-destaque")
        return "https://www.rogeriomenezes.com.br" + link_tag["href"] if link_tag else None
    
    def _getLote(self, resultado: Tag):
        link_tag = resultado.select_one("a.img-destaque")
        return link_tag["href"].split("/")[2] if link_tag else None
    
    def _getImgUrl(self, resultado: Tag):
        img_tag = resultado.select_one(".img img")
        return img_tag["src"] if img_tag else None
    
    def _getValorInicial(self, resultado: Tag):
        try:
            valor = resultado.select_one("p.lance-atual")
            return float(valor.text.replace("R$", "").replace(".", "").replace(",", ".")) if valor else "N/A"
        except Exception as e:
            return None
                
    def _getAno(self, title: str):
        ano_match = re.search(r"\b(19[0-9]{2}|20[0-9]{2})(\/(19[0-9]{2}|20[0-9]{2}))?\b", title)
        return ano_match.group(0) if ano_match else None
    
    def _getMarca(self, title):
        marca = title.split()[0]
        return marca
    
    def _getModelo(self, title):
        resultado = re.sub(r"^[A-Z]+\s", "", title)
        resultado = re.sub(r"\d{4}/\d{4}\s", "", resultado)
        return resultado

    # Função principal para processar os lotes
    def exec(self):

        # Realizar a requisição
        response = requests.get(self.url, headers=self.headers, params=self.params)

        if response.status_code != 200:
            print(f"Erro ao acessar o site: Status {response.status_code}")
            return []

        # Parsear o HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar os itens
        resultados = []
        for resultado in soup.select(".lote-item"):
            try:
                
                title = self._getTitle(resultado)
                link = self._getLink(resultado)
                lote = self._getLote(resultado)
                img_url = self._getImgUrl(resultado)
                ano = self._getAno(title)
                marca = self._getMarca(title)
                modelo = self._getModelo(title)                
                valor_atual = self._getValorInicial(resultado)
                
                
                # Se tem Marca
                existeMarca = next((m for m in self.Marcas if m["nome"].lower() in marca.lower()), None)
                
                if existeMarca:
                    marca = existeMarca["nome"].capitalize()
                
            
                if not existeMarca:
                    existeInModelo = next((m for m in self.Marcas if m["nome"].lower() in modelo.lower()), None)
                    marca = existeInModelo["nome"].capitalize()

            
                # Adicionar ao resultado
                resultados.append({
                    "uuid": str(uuid.uuid4()),
                    "lote": lote,
                    "chassi": None,
                    "valor_fipe": None,
                    "valor_atual": valor_atual,
                    "tipo_veiculo": None,
                    "marca": marca,
                    "modelo": modelo,
                    "monta" : getMonta(""),
                    "ano": ano,
                    "thumb": img_url,
                    "link": link,
                    "leiloeiro":"Rogério Menezes",
                    "ativo": 1,
                })
            except Exception as e:
                print(f"Erro ao processar um resultado: {e}")


        # print(json_output)
        return resultados


