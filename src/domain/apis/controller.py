from flask import Request
## APIS
from src.domain.apis.services.copart import ServiceCopart
from src.domain.apis.services.sodresantoro import ServiceSantoro
from src.domain.apis.services.freitas import ServiceFreitas
from src.domain.apis.services.palacio import ServicePalacios
from src.domain.apis.services.superbid import ServiceSuperBid
from src.domain.apis.services.joaoemilio import ServiceJoaoEmilio 
from src.domain.apis.services.rogeriomenezes import ServiceRogerio


class ApisController:

  def __init__(self, request: Request):
    self.request = request
  
  def exec(self):
    data = self.request.json
    query = data.get('query')
    api = data.get('api')
    print(f"Query recebida: {query}")
    
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
        case _:
            raise Exception("Api inválida.")
            

    return resultado
  