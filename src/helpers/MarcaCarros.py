
import json

def obter_marcas():
    # Abrir o arquivo JSON
    with open('src/store/Marcas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados

