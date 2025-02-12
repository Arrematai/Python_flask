
import json
import re


def obter_marcas():
    # Abrir o arquivo JSON
    with open('src/store/Marcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados

def marcaIsExiste(nome):
    # Abrir o arquivo JSON
    with open('src/store/Marcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    marca = any(m["nome"] == nome for m in dados)
    return nome if marca else None



## TROCA MARCA DENTRO DE UMA EXPRESSÃO
def replace_marcas(marca):
    # Abrir o arquivo JSON
    with open('src/store/replaceMarcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        
    for item in dados:
        nome = item["nome"]
        for termo in item["lista"]:
            if termo in marca:
                # Usa regex para substituir, ignorando maiúsculas/minúsculas
                texto = re.sub(rf'\b{re.escape(termo)}\b', nome, marca, flags=re.IGNORECASE)
                return texto
        
    return marca

## RETORNA A MARCA ENCONTRADA DENTRO DE UMA EXPRESSÃO       
def match_marca(marca:str):
    # Abrir o arquivo JSON
    with open('src/store/replaceMarcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
            
    for item in dados:
        nome = item["nome"]
        for termo in item["lista"]:
            if termo.upper() in marca.upper():
                return nome
        
    return None
        