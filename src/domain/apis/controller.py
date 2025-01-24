from flask import Request
import time
from flask_restful import Resource

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


class ApisController(Resource):
    

  def __init__(self, request: Request, ip: str):
    self.request = request
    self.Log = Log(ip)
  
  def exec(self):
    data = self.request.json
    query = data.get('query')
    api = data.get('api')
    print(f"Query recebida: {query}")
    print(f"Api recebida: {api}")
    start_time = time.time()
    
    match api:
        case "copart":
            copart = ServiceCopart(query,"2000")
            resultado = copart.exec() or []
        case "sodresantoro":
            santoro = ServiceSantoro(query,"2000")
            resultado = santoro.exec() or []
        case "palacio":
            palacios = ServicePalacios(query,"2000")
            resultado = palacios.exec()
        case "joaoemilio":
            joaoEmilio = ServiceJoaoEmilio(query,"2000")
            resultado = joaoEmilio.exec() or []
        case "superbid":
            superbid = ServiceSuperBid(query,"2000")
            resultado = superbid.exec() or []
        case "freitasleiloeiro":
            freitas = ServiceFreitas(query,"2000")
            resultado = freitas.exec() or []
        case "rogeriomenezes":
            rogerio = ServiceRogerio(query,"2000")
            resultado = rogerio.exec() or []
        case "liderleiloes":
            lider = ServiceLiderLeiloes(query,"2000")
            resultado = lider.exec() or []
        case "pestanaleiloes":
            pestana = ServicePestana(query,"2000")
            resultado = pestana.exec() or []
        case "vipleiloes":
            pestana = ServiceVip(query,"2000")
            resultado = pestana.exec() or []
        case _:
            raise Exception("Api inválida.")
            
    end_time = time.time()
    self.Log.executionTime(query=query, api=api,end=end_time, start=start_time)
    return resultado
  