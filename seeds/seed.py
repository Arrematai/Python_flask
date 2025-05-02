
import re
from urllib.parse import urlparse


from src.infra.database.mysql import DataBase
from src.infra.service.Parallelum import ServiceParallelum
# from src.helpers.seedDataBase import SeedDataBase

from src.domain.leiloeiros.repository import LeiloeirosRepository

def init():
  print("Inicio Aplicação")
  
  database = DataBase(dictionary=True)
  # service = ServiceParallelum()
  
  # seed = SeedDataBase(database=database, service=service)
  
  # seed.seedFipes()

  repository = LeiloeirosRepository(database)

  listLeiloeiros = repository.findLeiloeiros()


  for leiloeiro in listLeiloeiros:
    nome = clean_url(leiloeiro["site"])
    clear_nome = re.sub(r"leiloes?|leiloeiro?|leilao", "", nome, flags=re.IGNORECASE).strip()

    tags = leiloeiro["tag"].split(",") if leiloeiro["tag"] else []

    if clear_nome not in tags:
      newTags = ",".join(map(str, tags)) 
      valor = f"{clear_nome},{newTags}" if newTags else f"{clear_nome},"
      repository.updateTag(valor,leiloeiro["id"])
    

  print("Aplicação Finalizada")




def clean_url(url):
  # Parseia a URL para extrair o domínio
  parsed_url = urlparse(url)
  
  # Pega o netloc (domínio) ou, se não existir, usa a URL inteira
  domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path

  # Remove www. do início
  domain = re.sub(r"^www\.", "", domain)

  # Remove tudo depois do primeiro domínio de nível superior (TLD)
  domain = re.sub(r"\..*$", "", domain)

  # Remove qualquer barra final
  return domain.strip("/")