import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup
import urllib3
import uuid

from src.infra.helpers.MarcaCarros import obter_marcas
from src.infra.helpers.Monta import getMonta

# Desativando avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ServicePalacios:
    # url: Text = "https://www.palaciodosleiloes.com.br/site/camada_ajax/coluna_esquerda_m.php"
    url: Text = "https://api.scrapfly.io/scrape?tags=player%2Cproject%3Adefault&key=scp-live-0f1c0f0c671e457788540b8d2f1636e5&url=https%3A%2F%2Fwww.palaciodosleiloes.com.br%2Fsite%2Fcamada_ajax%2Fcoluna_esquerda_m.php"
    payload: Text
    params: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.Marcas = obter_marcas()
        self.initValue()
        
    def initValue(self):
        # self.params = {
        #         "quebra": "0.22699912025538405",
        #         "opcao": "listar_lote",
        #         "categoria_pesquisa": "",
        #         "subcategoria_pesquisa": "",
        #         "marca_pesquisa": "",
        #         "situacao_pesquisa": "",
        #         "local_pesquisa": "",
        #         "modelo_pesquisa": "",
        #         "ano_pesquisa": "",
        #         "cidade_site_pesquisa": "",
        #         "estado_site_pesquisa": "",
        #         "grupo_site_pesquisa": "",
        #         "txt_pesquisa_lote": {self.query},
        #         "leilao_pesquisa": "",
        #         "tipo_exibicao": "grid",
        #         "paginacao": "0",
        #         "total_paginas": "1",
        #         "somente_pesquisa": "0",
        #         "e_categoria": "1",
        #         "e_leilao": "1",
        #         "e_subcategoria": "0",
        #         "e_marca": "0",
        #         "e_modelo": "0",
        #         "e_ano": "0",
        #         "e_situacao": "0",
        #         "e_local": "0",
        #         "e_grupo": "0",
        #         "e_estado": "0",
        #         "e_cidade": "0"
        #     }
        self.payload = f"quebra=0.22699912025538405&&opcao=listar_lote&categoria_pesquisa=&subcategoria_pesquisa=&marca_pesquisa=&situacao_pesquisa=&local_pesquisa=&modelo_pesquisa=&ano_pesquisa=&cidade_site_pesquisa=&estado_site_pesquisa=&grupo_site_pesquisa=&txt_pesquisa_lote={self.query}&leilao_pesquisa=&tipo_exibicao=grid&paginacao=0&total_paginas=1&somente_pesquisa=0&e_categoria=1&e_leilao=1&e_subcategoria=0&e_marca=0&e_modelo=0&e_ano=0&e_situacao=0&e_local=0&e_grupo=0&e_estado=0&e_cidade=0"

        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Origin": "https://www.palaciodosleiloes.com.br",
            "Pragma": "no-cache",
            "Referer": f"https://www.palaciodosleiloes.com.br/site/leilao.php?txt_pesquisa_lote={self.query}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Cookie": "__goc_session__=celvfgfiytnepjfmgynsnaqowrkxrzvz; PHPSESSID=6mnan0gb5d25jg3ncdr6s5005m; _ga=GA1.1.1981685986.1743706519; _ga_2LQ3Q2WD1F=GS1.1.1743706519.1.1.1743706552.27.0.0"
        }
        
    def _getModelo(self,lote):
        modelo_completo = lote.select_one(".quebraln").text
        return " ".join(modelo_completo.split("/")[1:])
    
    def _getMarca(self,lote):
        modelo_completo = lote.select_one(".quebraln").text
        return modelo_completo.split("/")[0]
    
    def _getMonta(self,lote: BeautifulSoup):
        monta = lote.select_one(".mt-0.small")
        div = monta.find('div', class_="float-right")
        if div:
          div.extract()
        return getMonta(monta.get_text(strip=True))
    
    def _getValorInicial(self, lote):
        try: 
            valor_inicial_text = lote.find("div", class_="h3 mt-3 text-center").get_text(strip=True)
            numeros = re.findall(r'\d+[\.,]?\d*', valor_inicial_text)
            resultado = ','.join(numeros)
            return float(resultado.replace("R$", "").replace(".", "").replace(",", "."))  if resultado  else None 
        except Exception as e:
            return None
        
        
    def exec(self):
        resultados = []
        # response = requests.post(self.url, headers=self.headers, data=self.params)
        # lotes_html = response.text  # HTML da resposta

        response = requests.request("POST", self.url, data=self.payload)
        data = response.json()
        lotes_html = data["result"]["content"]

        soup = BeautifulSoup(lotes_html, 'html.parser')
        lotes = soup.select("div.col-md-3")
        

        for lote in lotes:
            
            modelo = self._getModelo(lote)
            marca = self._getMarca(lote)
            monta = self._getMonta(lote)
            
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
            
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": lote.select_one(".inf:-soup-contains('Lote') .float-right").text if lote.select_one(".inf:-soup-contains('Lote') .float-right") else "N/A",
                "chassi": None,
                "valor_fipe": None,
                "valor_atual":  self._getValorInicial(lote),
                "tipo_veiculo": None,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "ano": lote.select_one(".my-0.h6.mb-2").text,
                "thumb": f"https://www.palaciodosleiloes.com.br/site/{lote.select_one('img').get('src')}",
                "link": f"https://www.palaciodosleiloes.com.br/site/lotem.php?cl={lote.get('onclick').split('(')[-1].split(',')[0]}",
                "leiloeiro":"Palácio dos Leilões",
                "ativo": 1,
            }
            
            # Adiciona o dicionário à lista de resultados
            resultados.append(resultado)


        print(len(resultados))
        # return jsonify(resultados)
        return resultados

