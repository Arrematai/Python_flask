import json
import os


def SaveML(resultados, arquivo_saida):
    # Tentar carregar dados existentes
    if os.path.exists(arquivo_saida):
        with open(arquivo_saida, 'r', encoding='utf-8') as f:
            dados_existentes = json.load(f)
    else:
        dados_existentes = []

    # Transformar novos resultados no formato desejado
    novos_dados = []
    for item in resultados:
        dado = {
            "json": json.dumps({
                "marca": item.get("marca"),
                "modelo": item.get("modelo")
            }),
            "marca": item.get("marca"),
            "modelo": item.get("modelo")
        }
        # Evitar duplicatas
        if dado not in dados_existentes:
            novos_dados.append(dado)

    # Combinar dados existentes com novos
    dados_totais = dados_existentes + novos_dados

    # Salvar no arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_totais, f, ensure_ascii=False, indent=4)

    print(f"{len(novos_dados)} novos registros adicionados ao arquivo: {arquivo_saida}")

# Exemplo de uso
if __name__ == "__main__":
    # Chamar a API com uma query de exemplo
    query = "BMW"
    resultados = Copart(query)

    # Definir o nome do arquivo de saída
    arquivo_saida = "dados_treinamento.json"

    # Salvar os resultados no formato de treinamento
    SaveML(resultados, arquivo_saida)