import requests

class ServiceParallelum:
    urlApi = "https://parallelum.com.br/fipe/api/v1/carros"
    
    def get(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # return response.json()
                responseJson = response.json()
                
                return responseJson

            else:
                print(f"Erro ao acessar a API FIPE: Status {response.status_code}")
                raise Exception("Erro de retorno da API")
        except Exception as e:
            print(f"Erro ao conectar à API FIPE: {e}")
            raise Exception("erro em se conectar a API.")
    
    
    # Função para obter marcas de veículos da API FIPE
    def getMarcas(self):
        ## https://parallelum.com.br/fipe/api/v1/carros/marcas
        marcas = self.get(f"{self.urlApi}/marcas")
        substituicoes = {
            "GM - Chevrolet": "Chevrolet",
            "VW - VolksWagen": "Volkswagen",
            "Mercedes-Benz": "Mercedes",
            "Rolls-Royce": "Rolls",
            "Caoa Chery/Chery": "Chery",
            "Citroën": "Citroen"
        }
        for marca in marcas:
            if marca['nome'] in substituicoes:
                marca['nome'] = substituicoes[marca['nome']]
        return marcas
        
    def getModelos(self,marcaID):
        ## https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos
        modelos = self.get(f"{self.urlApi}/marcas/{marcaID}/modelos")
        
        if "modelos" in modelos:
            return modelos["modelos"]
        else:
            raise Exception("erro em retornar modelos.")
        
    
    def getAnos(self,marcaID,modeloID):
        ## https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos
        anos = self.get(f"{self.urlApi}/marcas/{marcaID}/modelos/{modeloID}/anos")
        return anos
    
    def getFipe(self,marcaID,modeloID,codigoAno):
        #GET: https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos/2014-3   
        fipe = self.get(f"{self.urlApi}/marcas/{marcaID}/modelos/{modeloID}/anos/{codigoAno}")
        return fipe