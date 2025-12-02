from datetime import datetime
import re
from typing import Text
import requests
import uuid
from src.infra.helpers.Monta import getMonta

from src.domain.lotes.repository import LotesRepository
from src.domain.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.infra.service.Logging import Log



class SchedulerPestana:
    url: Text = 'https://www.pestanaleiloes.com.br/api/v2/lote'
    payload: Text
    headers: Text
    resultados: list = []

    def __init__(self, scheduler: str, schedulerLogRepository: SchedulersLogRepository, lotesRepository: LotesRepository):
        self.scheduler = scheduler
        self.schedulerLogRepository = schedulerLogRepository
        self.lotesRepository = lotesRepository
        self.size = 9999
        self.resultados = []
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.headers= {}

    def sincronizar(self, dados_db, dados_novos):

        def chave_composta(item):
            return (item['lote'], item["marca"], item["modelo"], item['ano'])
            # return (item['descricao'])

        db_map = {chave_composta(item): item for item in dados_db}
        novos_map = {chave_composta(item): item for item in dados_novos}

        inserir = []
        atualizar = []
        remover = []

        # campos_para_verificar = ["lote",'marca', 'modelo', 'ano',"ativo"]
        campos_para_verificar = ['descricao',"lote", "ativo"]

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

    def exec (self):
        print("INICIADO SCHEDULER PESTANA")
        response = requests.get(self.url, headers=self.headers)
        
        if response.status_code != 200:
            self.log.SchedulerError(self.scheduler, response.status_code)
            self.schedulerLogRepository.insertLog({ 
                "nome": self.scheduler,
                'status': 'error',
                "duration": 0,
                "results": 0
                })
            return
        
          
        data = response.json()
        
        
        automoveis = list(filter(lambda item: item["bens"][0]["tipoBem"]["id"] == 421, data))
        
        if automoveis and len(automoveis) > 0:
          for automovel in automoveis:
              
            descricao = automovel.get("descricao")
            valor_atual = automovel.get("valorInicial")
            leilao = automovel.get("leilao")
            lote = automovel.get("id")
            link = f"https://www.pestanaleiloes.com.br/agenda-de-leiloes/{leilao}/{lote}"
            
            tipo_veiculo = None
            try:
                tipo_veiculo = automovel["bens"][0]["subTipoBem"]["nome"]
            except (KeyError, IndexError, TypeError):
                tipo_veiculo = None
            
            
            condicao = None
            try:
                condicao = automovel["bens"][0]["origem"]
            except (KeyError, IndexError, TypeError):
                condicao = None
            
            thumb = None
            try:
                thumb = automovel["bens"][0]["imagens"][0]["original"]
            except (KeyError, IndexError, TypeError):
                thumb = None
            
            cidade = None
            try:
                cidade = automovel["bens"][0]["cidade"]["name"]
            except (KeyError, IndexError, TypeError):
                cidade = None
                
            estado = None
            try:
                estado = automovel["bens"][0]["estado"]["name"]
            except (KeyError, IndexError, TypeError):
                estado = None
            
            caracteristicas = automovel["bens"][0]["caracteristicas"]
            
            
            kilometragem = next(
            (item["valor"] for item in caracteristicas if item["icone"] == "MdOutlineSpeed"),
            None
            )
            
            monta = next(
            (item["valor"] for item in caracteristicas if item["icone"] == "MdOutlineDirectionsCarFilled"),
            None
            )
            
            transmissao = next(
            (item["valor"] for item in caracteristicas if item["icone"] == "MdOutlineMiscellaneousServices"),
            None
            )
            
            cor = next(
            (item["valor"] for item in caracteristicas if item["icone"] == "MdOutlineColorLens"),
            None
            )
            
            placa = next(
            (item["valor"] for item in caracteristicas if item["icone"] == "MdOutlinePin"),
            None
            )
            
            combustivel = next(
            (item["valor"] for item in caracteristicas if item["icone"] == "MdOutlineLocalGasStation"),
            None
            )
            
            itens_carro = [item for item in caracteristicas if item["icone"] == "MdOutlineDirectionsCarFilled"]
        
            
            # garantir que existam 3 itens
            marca = itens_carro[1]["valor"] if len(itens_carro) > 1 else None
            modelo = itens_carro[2]["valor"] if len(itens_carro) > 2 else None
            versao = itens_carro[3]["valor"] if len(itens_carro) > 3 else None
            
            
            anos = [item for item in caracteristicas if item["icone"] == "MdOutlineCalendarToday"]
            
            ano1 = anos[0]["valor"] if len(anos) > 0 else None
            ano2 = anos[1]["valor"] if len(anos) > 0 else None
                
            thumb = f"https://ged.pestanaleiloes.com.br/ged/{thumb}"
                
                
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote":  lote,
                "chassi": "",
                "descricao": f"{marca} {modelo} {ano1}/{ano2} {cor}",
                "valor_fipe": None,
                "valor_atual": valor_atual,
                "tipo_veiculo": tipo_veiculo,
                "marca": marca,
                "modelo": f'{modelo} {versao}',
                "monta": getMonta(monta),
                "condicao": condicao,
                "ano": f'{ano1}/{ano2}',
                "thumb": thumb,
                "link": link,
                "cor": cor,
                "combustivel": combustivel,
                "kilometragem": kilometragem,
                "transmissao": transmissao,
                "placa": placa,
                "cidade": cidade,
                "estado": estado,
                "leiloeiro":"Pestana Leilões",
                "api":self.scheduler,
                "ativo": 1,
            }

    
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
        print("FINALIZADO SCHEDULER PESTANA")
