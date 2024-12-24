import requests

# Função para obter marcas de veículos da API FIPE
def obter_marcas_fipe():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # return response.json()
            lista_marcas = response.json()

            substituicoes = {
                "GM - Chevrolet": "Chevrolet",
                "VW - VolksWagen": "Volkswagen",
                "Mercedes-Benz": "Mercedes",
                "Rolls-Royce": "Rolls",
                "Caoa Chery/Chery": "Chery",
                "Citroën": "Citroen"
            }

            for marca in lista_marcas:
                if marca['nome'] in substituicoes:
                    marca['nome'] = substituicoes[marca['nome']]

            return lista_marcas

        else:
            print(f"Erro ao acessar a API FIPE - MARCA: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao conectar à API FIPE: {e}")
        return []

# def obter_modelos_fipe(codigo_marca):
#     url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             # Retornar apenas os nomes dos modelos
#             return [modelo["nome"].split()[0] for modelo in response.json()["modelos"]]

#         else:
#             print(f"Erro ao acessar a API FIPE - MODELO: Status {response.status_code}")
#             return []
#     except Exception as e:
#         print(f"Erro ao conectar à API FIPE: {e}")
#         return []

def obter_modelos_fipe(codigo_marca):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Retornar apenas os nomes dos modelos
            lista = response.json()
            return lista["modelos"]

        else:
            print(f"Erro ao acessar a API FIPE - MODELO: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao conectar à API FIPE: {e}")
        return []