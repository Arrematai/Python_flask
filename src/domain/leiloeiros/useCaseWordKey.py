import Levenshtein
from difflib import SequenceMatcher, get_close_matches
from itertools import chain
import re

      
   
def UseCaseWordKey(self, wordKey: str, listLeiloeiros):
  try:
    resultadosUniques = []
    resultados = []
    chaves_vistas = set()
    cutoff = 0.7
    
    resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "site",cutoff)))
    resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "email",cutoff )))
    resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "nome", cutoff)))
    resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "tag", cutoff)))
    if len(resultados) > 0:
      for obj in resultados:
        chave = (obj["id"])  # Defina os campos que devem ser considerados únicos
        if chave not in chaves_vistas:
            chaves_vistas.add(chave)
            resultadosUniques.append(obj)
            
      return ("algoritmo-lvl1", sorted(resultadosUniques, key=lambda x: x['nota'], reverse=True))
    
    while cutoff >= 0.5:
      ## search NOME OR EMAIL OR SITE  
      resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "site", cutoff)))
      resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "email", cutoff)))
      resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "nome", cutoff)))
      resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "tag", cutoff)))
      
      for obj in resultados:
          chave = (obj["id"])  # Defina os campos que devem ser considerados únicos
          if chave not in chaves_vistas:
              chaves_vistas.add(chave)
              resultadosUniques.append(obj)
            
      cutoff = cutoff - 0.1
    
    return ("algoritmo-lvl2", sorted(resultadosUniques, key=lambda x: x['nota'], reverse=True))
  except Exception as e:
    print("ERROR:",e)
    raise Exception("Nem um leiloeiro encontrado na busca.")
  
  
# Função para encontrar a string mais parecida
def moreSimilarWordsLevenshtein(self, wordKey: str, lista: list, key: str):
  similares = []
  shortestDistance = 5

  for item in lista:
    palavra: str = item[key]
    distancia = Levenshtein.distance(wordKey.lower(), palavra.lower().replace(" ", ""))
    # print(wordKey, item[key], distancia)
    if distancia <= shortestDistance:
        similares.append((item, distancia))

  return sorted(similares, key=lambda x: x[1])

# Função para calcular a similaridade entre duas strings
def calcSimilaridade(self,a, b):
    return SequenceMatcher(None, a, b).ratio()

# Função para encontrar todas as strings similares
def moreSimilarWords(self, string_base: str, lista: list, key: str, limite=0.25):
    similares = []
    for item in lista:
        similaridade = self.calcSimilaridade(string_base.lower(), item[key].lower())
        # print(string_base, item[key], similaridade)
        if similaridade >= limite:
            similares.append(item)
    return similares
  
def moreSimilarWordsCutOff(self, string_base: str, lista: list, key: str, cutoff=0.1):
  resultados = []
  resultados_unicos = []
  objetos_filtrados = []
  listKey = [obj[key].upper() for obj in lista]
  
  ## procura as palavras similares
  for item in listKey:
    palavras = re.split(r'[@.\s]+|leiloes|lei|WWW|COM|BR', item, flags=re.IGNORECASE)
    resultado_value = get_close_matches(string_base.upper(), palavras, n=1, cutoff=cutoff)
    if len(resultado_value) > 0: 
      # print(resultado_value,cutoff, self.calcSimilaridade(string_base.lower(), resultado_value[0].lower()))
      # print({key: resultado_value[0], "nota": self.calcSimilaridade(string_base.lower(), resultado_value[0].lower())})
      resultados.append({key: resultado_value[0], "nota": self.calcSimilaridade(string_base.lower(), resultado_value[0].lower())})
  
  
  ## remove duplicados
  chaves_vistas = set()
  for obj in resultados:
    chave = (obj[key])  # Defina os campos que devem ser considerados únicos
    if chave not in chaves_vistas:
        chaves_vistas.add(chave)
        resultados_unicos.append(obj)
        

  ## pegar o objeto vinculado a palavra
  for obj in lista:
    # Verificando se o nome completo ou parte dele está no array
    if any(palavra in [ru[key] for ru in resultados_unicos] for palavra in obj[key].split()):
      nota = None
      for resultado in resultados_unicos:
        if resultado[key] in obj[key].split():
          nota = resultado["nota"]
      
      obj["nota"] = nota
      objetos_filtrados.append(obj)

  
  return objetos_filtrados

def moreSimilarWord(self, string_base: str, lista: list, key: str, limite=0.6):     
  similares = []
  for item in lista:
      palavras = re.split(r'[@.\s]+|leiloes|lei|WWW|COM|BR', item[key], flags=re.IGNORECASE)
      for palavra in palavras:
        similaridade = self.calcSimilaridade(string_base.lower(), palavra.lower())
        if similaridade >= limite:
          # print(string_base.lower(),palavra.lower(),similaridade)
          item['nota'] = similaridade
          similares.append(item)
  return similares