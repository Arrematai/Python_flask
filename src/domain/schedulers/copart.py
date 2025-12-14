from datetime import datetime, timedelta
import os
# import logging
from typing import Text
import requests
import uuid

from src.domain.lotes.repository import LotesRepository
from src.domain.schedulers.sincronizar import sincronizar
from src.domain.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log

class SchedulerCopart:
    url: Text = 'https://www.copart.com.br/public/lots/search'
    payload: Text
    headers: Text

    def __init__(self, scheduler: str, schedulerLogRepository: SchedulersLogRepository, lotesRepository: LotesRepository):
        self.scheduler = scheduler
        self.schedulerLogRepository = schedulerLogRepository
        self.lotesRepository = lotesRepository
        self.resultados = []
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.payload = f"page=0&size=100000&freeFormSearch=true&filter[tipovenda]=tipovenda:Leilão&filter[upcominglots]=exclude_upcoming_lots:*"
        self.headers= {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "visid_incap_1046344=UnXbvuBQTcWGX9QXlhvawTQ9cmYAAAAAQUIPAAAAAABneqsCps9dLCbwqh9Q2UCx; _fbp=fb.2.1718762814309.23790209733670714; tt.u=0100007FD1317266E906033802B9AF11; rdtrk=%7B%22id%22%3A%227c755536-f5cf-434b-a4c2-4cf353b6d28a%22%7D; OAID=e545c6c595a605e76211455399bdf6b1; userCategory=RPU; g2app.username=; _ga=GA1.1.134325795.1718762814; _ga_63JLT6J1TE=deleted; g2app.acceptCookiePolicy=true; copartbrmember=00df814ca4b576071d1e8881929849e1; userLang=pt_BR; nlbi_1046344=dglaJdTHExLmsrrhMphbYQAAAAAkfSnlclBRroFe5eRSxOv4; g1usersessionid=859d302ca4065527a192cb3db8535491; usersessionid=a464acc53ef4b4804afa8864eaa2ad5e; OAGEO=BR%7CMinas+Gerais%7CNazareno%7C37220-000%7C-21.21639%7C-44.61139%7C%7C035%7C%7CConecta+Ltda.%7CDSL; G2MBRJSESSIONID=5739CB681889EF83A479ACFEAC4C5930-n1; C2BID=705069; cmRzdGF0aW9uLXBvcHVwLTY0Mzg1NDQtdmlld2Vk=viewed; incap_ses_987_1046344=Pb8DBaHyE1YJgjhRYYeyDesCMWcAAAAABw5K1O8U0lxNBGq5cKdS9w==; tt_c_vmt=1731265877; tt_c_c=direct; tt_c_s=direct; tt_c_m=direct; tt.nprf=; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Nov+10+2024+16%3A17%3A18+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202403.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&consentId=de1deaf4-debd-43e1-9645-15039e57d959&interactionCount=0&isAnonUser=1; _ttuu.s=1731266240543; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiKG5vbmUpIiwiZXh0cmFfcGFyYW1zIjp7fX0sImNyZWF0ZWRfYXQiOjE3MzEyNjYyNDA1NTF9; _gcl_au=1.1.294617627.1726801367.877339667.1731265261.1731266249; _ga_63JLT6J1TE=GS1.1.1731265260.23.1.1731266711.60.0.1000883153",
            "Origin": "https://www.copart.com.br",
            "Referer": f"https://www.copart.com.br/lotSearchResults/?free=true&searchCriteria=%7B%22query%22:%5B%22bmw%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:true%7D",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-TOKEN": "null"
        }
        
    def exec (self):
        print("INICIADO SCHEDULER COPART", datetime.now())
        response = requests.post(self.url, data=self.payload, headers=self.headers)
        
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
        
        for item in data.get('data', {}).get('results', {}).get('content', []):
            lote = item.get("lotNumberStr", None)
            chassi = item.get("fv", None)
            valor_fipe = item.get("la", None)
            valor_atual = item.get("hb", None)
            tipo_veiculo = item.get("vehicleType", None)
            marca = item.get("mkn", None)
            modelo = item.get("lm", None)
            monta = getMonta(item.get("damageClassification", None))
            ano = item.get("manufactureYear", None)
            thumb = item.get("tims").replace("thumbnail","vga")
            data_leilao = item.get("ad", None) if item.get("ad", None) and item.get("ad") != ""  else None
            local = item.get("yn", None)
            cidade, estado = (local.split(" - ") + [""])[:2]
            condicao = item.get("lossType", None)
            
            descricao = f"{marca} - {modelo} - {ano} - {chassi}"
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "descricao": descricao,
                "data_leilao": data_leilao,
                "cidade": cidade,
                "estado": estado,
                "condicao": condicao,
                "lote": lote, 
                "chassi": chassi,
                "valor_fipe": valor_fipe,
                "valor_atual": valor_atual,
                "tipo_veiculo": tipo_veiculo,
                "marca": marca ,
                "modelo": modelo,
                "monta": monta,
                "ano": ano ,
                "cor": None,
                "combustivel": None,
                "kilometragem": None,
                "transmissao": None,
                "thumb": thumb,
                "link": "https://www.copart.com.br/lot/" + str(item.get("lotNumberStr")),
                "leiloeiro":"COPART",
                "api":self.scheduler,
                "ativo": 1,
            }
            # Adiciona o dicionário à lista de resultados
            self.resultados.append(resultado)
            
        dbLotes = self.lotesRepository.getLotesByApi(self.scheduler)
        inserir,atualizar, remover = sincronizar(dbLotes, self.resultados)

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
        print("FINALIZADO SCHEDULER COPART")
