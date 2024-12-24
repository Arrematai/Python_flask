
import json

def obter_modelos(modelo: str):
    # Abrir o arquivo JSON
    with open(f'src/store/modelos/{modelo}.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

    return dados

