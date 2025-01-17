import time

## INFRA
from src.infra.service.Logging import Log

## APIS
from src.domain.apis.services.copart import ServiceCopart
from src.domain.apis.services.sodresantoro import ServiceSantoro
from src.domain.apis.services.freitas import ServiceFreitas
from src.domain.apis.services.palacio import ServicePalacios
from src.domain.apis.services.superbid import ServiceSuperBid
from src.domain.apis.services.joaoemilio import ServiceJoaoEmilio
from src.domain.apis.services.rogeriomenezes import ServiceRogerio
from src.domain.apis.services.liderleiloes import ServiceLiderLeiloes
from src.domain.apis.services.pestana import ServicePestana
from src.domain.apis.services.vipleiloes import ServiceVip
# from src.domain.apis.services.kuss import ServiceKuss
# from src.domain.apis.services.mgl import MGL



def init():
  print("Inicio Aplicação TESTE")
  start_time = time.time()
  log = Log("TESTE")
  
  palacios = ServicePalacios("fiat", 2000)  
  result = palacios.exec()
  
  # freitas = ServiceFreitas("fiat", 2000)  
  # result = freitas.exec()
  
  # joao = ServiceJoaoEmilio("fiat", 2000)
  # result = joao.exec()
  
  # palacios = ServicePalacios("fiat", 2000)  
  # result = palacios.exec()
  
  # lider = ServiceLiderLeiloes("fiat", 2000)  
  # result = lider.exec()
  
  # pestana = ServicePestana("bmw", 2000)  
  # result = pestana.exec()
  
  # vip = ServiceVip("fiat", 2000)  
  # result = vip.exec()

  # print("Resultados:",result)
  end_time = time.time()
  log.executionTime(query="fiat", api="TESTE",end=end_time, start=start_time)
  print("Aplicação Finalizada TESTE")