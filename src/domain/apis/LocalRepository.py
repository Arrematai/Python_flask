
import json
import re


def obter_apis():
    # Abrir o arquivo JSON
    with open('src/store/Apis.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados

