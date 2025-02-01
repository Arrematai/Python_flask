
import json
import re


def obter_marcas():
    # Abrir o arquivo JSON
    with open('src/store/Marcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados


def replace_marcas(marca):
    # Abrir o arquivo JSON
    with open('src/store/replaceMarcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        
    for item in dados:
        nome = item["nome"]
        for termo in item["lista"]:
            # Usa regex para substituir, ignorando maiúsculas/minúsculas
            texto = re.sub(rf'\b{re.escape(termo)}\b', nome, marca, flags=re.IGNORECASE)
            return texto
        
    return marca
        