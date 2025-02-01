
import json

def obter_pecas():
    # Abrir o arquivo JSON
    with open('src/store/pecas.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados

