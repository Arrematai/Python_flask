from src.infra.service.Parallelum import obter_modelos_fipe
from src.helpers.MarcaCarros import obter_marcas
import json
import time

def createdFilesModelosMarcas():
  marcas = obter_marcas()
  
  for marca in marcas:
    print(f"{marca["nome"]} - ","___________________________________________________")
    print(f"{marca["nome"]} - ","RODANDO MARCA")
    modelos = obter_modelos_fipe(marca["codigo"])
    
    with open(f'src/store/modelos/{marca["nome"].replace("/", "-")}.json' , "w", encoding="utf-8") as arquivo:
      json.dump(modelos, arquivo, ensure_ascii=False, indent=4)
      print(f"{marca["nome"]} - ","ARQUIVO CRIADO E SALVO")
    
    print(f"{marca["nome"]} - ","___________________________________________________")
    time.sleep(10)
  
  
