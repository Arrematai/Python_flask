from datetime import datetime 
import uuid
from typing import Text
import re
from bs4 import BeautifulSoup
import uuid
from urllib.parse import parse_qs



from src.infra.helpers.MarcaCarros import obter_marcas
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log
from src.infra.service.ScrapeDo import ScrapeDo
from src.domain.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.domain.lotes.repository import LotesRepository



class SchedulerPalacio:
    url: Text = "https://www.palaciodosleiloes.com.br/site/camada_ajax/coluna_esquerda_m.php"
    payload: Text
    params: Text
    headers: Text

    def __init__(self, scheduler: str, schedulerLogRepository: SchedulersLogRepository, lotesRepository: LotesRepository):
        self.scheduler = scheduler
        self.schedulerLogRepository = schedulerLogRepository
        self.lotesRepository = lotesRepository
        self.size = 9999
        self.Marcas = obter_marcas()
        self.resultados = []
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.payload = {f"quebra": "0.9389920978354351", "opcao": "listar_lote", "categoria_pesquisa": "1",
                   "subcategoria_pesquisa": "", "marca_pesquisa": "", "situacao_pesquisa": "", "local_pesquisa": "",
                   "modelo_pesquisa": "", "ano_pesquisa": "", "grupo_site_pesquisa": "",
                   "leilao_pesquisa": "", "tipo_exibicao": "grid", "paginacao": "-1", "total_paginas": "999",
                   "somente_pesquisa": "0", "e_categoria": "1", "e_leilao": "1", "e_subcategoria": "0", "e_marca": "0",
                   "e_modelo": "0", "e_ano": "0", "e_situacao": "0", "e_local": "0", "e_grupo": "0"}
        
        self.params = f"=&opcao=listar_lote&categoria_pesquisa=&subcategoria_pesquisa=&marca_pesquisa=&situacao_pesquisa=&local_pesquisa=&modelo_pesquisa=&ano_pesquisa=&grupo_site_pesquisa=&leilao_pesquisa=&tipo_exibicao=grid&paginacao=-1&total_paginas=999&somente_pesquisa=0&e_categoria=1&e_leilao=1&e_subcategoria=0&e_marca=0&e_modelo=0&e_ano=0&e_situacao=0&e_local=0&e_grupo=0"

        
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Origin": "https://www.palaciodosleiloes.com.br",
            "Pragma": "no-cache",
            "Referer": f"https://www.palaciodosleiloes.com.br/site/leilao.php?categoria_pesquisa=1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Cookie": "__goc_session__=celvfgfiytnepjfmgynsnaqowrkxrzvz; PHPSESSID=6mnan0gb5d25jg3ncdr6s5005m; _ga=GA1.1.1981685986.1743706519; _ga_2LQ3Q2WD1F=GS1.1.1743706519.1.1.1743706552.27.0.0"
        }
        
    def _getModelo(self,lote):
        modelo_completo = lote.select_one(".quebraln").text
        return " ".join(modelo_completo.split("/")[1:])
    
    def _getMarca(self,lote):
        IGNORAR = {"I", "R", "LR", "I/LR", "SR"}
        modelo = lote.select_one(".quebraln").text.strip()
        linha = modelo.strip()

        # separa antes/depois da barra
        if "/" not in linha:
            return linha.split()[0].upper()

        antes, depois = linha.split("/", 1)

        # primeira marca da esquerda
        marca_esq = antes.strip().split()[0].upper()

        # se a marca da esquerda for falsa (I, R, LR) → pega a real após a barra
        if marca_esq in IGNORAR:
            return depois.strip().split()[0].upper()
        return marca_esq
    
    def _getMonta(self,lote: BeautifulSoup):
        monta = lote.select_one(".mt-0.small")
        div = monta.find('div', class_="float-right")
        if div:
          div.extract()
        return getMonta(monta.get_text(strip=True) or "")
    
    def _getValorInicial(self, lote):
        try: 
            valor_inicial_text = lote.find("div", class_="h3 mt-3 text-center").get_text(strip=True)
            numeros = re.findall(r'\d+[\.,]?\d*', valor_inicial_text)
            resultado = ','.join(numeros)
            return float(resultado.replace("R$", "").replace(".", "").replace(",", "."))  if resultado  else None 
        except Exception as e:
            return None
        
    def _getLink(self,lote):
        div = lote.find("div", class_="i-c")
        onclick = div.get('onclick')
                    
        if(onclick):
            return onclick.split('(')[-1].split(',')[0]
        
        return None
    
    def _getDataLeilao(self,lote):
        data = lote.find_all("div", class_="float-right")
        
        if data and len(data) > 0:
            return data[1].text.strip()

        return None
    
    def _getLeilao(self,lote):
        data = lote.find_all("div", class_="float-right")
        
        if data and len(data) > 0:
            return data[0].text.strip()

        return None
        
    def sincronizar(self, dados_db, dados_novos):

        def chave_composta(item):
            return (item['lote'], item['leilao'], item["marca"], item["modelo"], item['ano'])
            # return (item['descricao'])

        db_map = {chave_composta(item): item for item in dados_db}
        novos_map = {chave_composta(item): item for item in dados_novos}

        inserir = []
        atualizar = []
        remover = []

        # campos_para_verificar = ['marca', 'modelo', 'ano', 'chassi',"ativo"]
        campos_para_verificar = ['descricao',"ativo"]

        # --- 1) VERIFICAR INSERÇÃO E ATUALIZAÇÃO ---
        for chave, novo in novos_map.items():

            # Caso ainda não exista → inserir
            if chave not in db_map:
                inserir.append(novo)
                continue

            # Caso exista → verificar alterações
            antigo = db_map[chave]
            diff = any(
                novo.get(k) != antigo.get(k)
                for k in campos_para_verificar
            )
            if diff:
                novo["id"] = antigo.get("id")
                novo["uuid"] = antigo.get("uuid")
                atualizar.append(novo)

        # --- 2) VERIFICAR REMOÇÃO POR NÃO EXISTIR MAIS ---
        for chave, antigo in db_map.items():
            if chave not in novos_map:
                remover.append(antigo)

        return inserir, atualizar, remover
        
    def exec(self):
        print("INICIADO SCHEDULER PALACIO")
        #response = requests.request("POST", self.url, data=self.payload)

        # response = ScrapflyScrape("POST", self.url, self.payload, self.headers
        # response = ScrapingbeeScrape("POST", self.url, self.payload, self.headers)
        response = ScrapeDo("POST", self.url, self.payload, self.headers)

  
        if response.status_code != 200:
            self.log.SchedulerError(self.scheduler, response.status_code)
            self.schedulerLogRepository.insertLog({ 
                "nome": self.scheduler,
                'status': 'error',
                "duration": 0,
                "results": 0
                })
            return

        lotes_html = response.content

        soup = BeautifulSoup(lotes_html, 'html.parser') 
        lotes = soup.select("div.col-md-3")
        
        
        
        for lote in lotes:
            
            modelo = self._getModelo(lote)
            marca = self._getMarca(lote)
            monta = self._getMonta(lote)
            data_leilao = self._getDataLeilao(lote)
            leilao = self._getLeilao(lote)
            loteId = lote.select_one(".inf:-soup-contains('Lote') .float-right").text if lote.select_one(".inf:-soup-contains('Lote') .float-right") else "N/A"
            ano = lote.select_one(".my-0.h6").text
            thumb = f"https://www.palaciodosleiloes.com.br/site/{lote.select_one('img').get('src')}"
            link = f"https://www.palaciodosleiloes.com.br/site/lotem.php?cl={self._getLink(lote)}"
            
            # Se nao tem marca nem modelo
            if not marca and not modelo or (not modelo):
                continue
            
            # # # Se tem Marca
            # existeMarca = next((m for m in self.Marcas if m["nome"].lower() in marca.lower()), None)


            # if existeMarca:
            #     marca = existeMarca["nome"].capitalize()
            
            # print(marca)

            # if not existeMarca:
            #     existeInModelo = next((m for m in self.Marcas if m["nome"].lower() in modelo.lower()), None)
            #     marca = existeInModelo["nome"].capitalize()
            
            
            data_dt = datetime.strptime(data_leilao, "%d/%m/%y")
            data_mysql = data_dt.strftime("%Y-%m-%d 08:00:00")
            
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "leilao": leilao,
                "descricao": f"{leilao}, {loteId}, {marca}, {modelo}, {ano}",
                "lote": loteId,
                "chassi": None,
                "valor_fipe": None,
                "valor_atual":  self._getValorInicial(lote),
                "tipo_veiculo": None,
                "data_leilao": data_mysql,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "ano": ano,
                "thumb": thumb,
                "link": link,
                "leiloeiro":"Palácio dos Leilões",
                "api":self.scheduler,
                "ativo": 1,
            }
            
            # Adiciona o dicionário à lista de resultados
            self.resultados.append(resultado)

        dbLotes = self.lotesRepository.getLotesByApi(self.scheduler)
        inserir,atualizar, remover = self.sincronizar(dbLotes, self.resultados)

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
        print("FINALIZADO SCHEDULER PALACIO")

