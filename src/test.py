## APIS
from src.services.copart import ServiceCopart
from src.services.sodresantoro import ServiceSantoro
from src.services.freitas import ServiceFreitas
from src.services.palacio import ServicePalacios
from src.services.superbid import ServiceSuperBid
from src.services.joaoemilio import ServiceJoaoEmilio 
from src.services.rogeriomenezes import ServiceRogerio
from src.services.mgl import MGL



def init():
  print("Inicio Aplicação")
  
  mgl = MGL("fiat")
  

  print("Aplicação Finalizada")