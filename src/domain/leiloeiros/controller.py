import Levenshtein
from difflib import SequenceMatcher, get_close_matches
from itertools import chain
import re

from src.infra.database.mysql import DataBase
from src.domain.leiloeiros.repository import LeiloeirosRepository



class LeiloeirosController:

  def __init__(self, database: DataBase):
    self.database = database
    self.repository = LeiloeirosRepository(self.database)
  
  def getLeiloeiros(self):  
      try:
        result = self.repository.findLeiloeiros()
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise("Teste Controller Leiloeiro")
        
  def getLeiloeirosByEstado(self, estado):
      try:
        result = self.repository.filterByEstado(estado)
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise("Teste Controller Leiloeiro")
        
  def getEstados(self):
      try:
        result = self.repository.filterEstados()
        
        return result
            
      except Exception as e:
          print(f"Error: {e}")
          raise("Teste Controller Leiloeiro")
        
        
  def getByWordKey(self, wordKey: str):
    try:
      newListLeiloeiros = self.repository.getLeiloeirosByWordKey(wordKey)
      
    
      if newListLeiloeiros and len(newListLeiloeiros) > 0:
        return ("banco", newListLeiloeiros)
      
      listLeiloeiros = self.getLeiloeiros()
      resultadosUniques = []
      resultados = []
      chaves_vistas = set()
      cutoff = 0.5
        
      resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "nome")))
      resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "site")))
      resultados = list(chain(resultados, self.moreSimilarWord(wordKey, listLeiloeiros, "email")))
      if len(resultados) > 0:
        for obj in resultados:
          chave = (obj["id"])  # Defina os campos que devem ser considerados únicos
          if chave not in chaves_vistas:
              chaves_vistas.add(chave)
              resultadosUniques.append(obj)
        return ("algoritmo-lvl1", resultadosUniques)
      
      
      while cutoff >= 0.3 or len(resultados) >= 5:
        ## search NOME OR EMAIL OR SITE  
        resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "nome", cutoff)))
        resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "site", cutoff)))
        resultados = list(chain(resultados, self.moreSimilarWordsCutOff(wordKey, listLeiloeiros, "email", cutoff)))
        
        for obj in resultados:
            chave = (obj["id"])  # Defina os campos que devem ser considerados únicos
            if chave not in chaves_vistas:
                chaves_vistas.add(chave)
                resultadosUniques.append(obj)
              
        print(cutoff)
        cutoff = cutoff - 0.05
      
      return ("algoritmo-lvl2", resultadosUniques)
    except Exception as e:
      print("ERROR:",e)
    
    
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
    listKey = [obj[key].upper() for obj in lista]
    
    # for item in listKey:
    #   print(string_base, item, self.calcSimilaridade(string_base.lower(), item.lower()))

    resultados_value = get_close_matches(string_base.upper(), listKey, n=10000, cutoff=cutoff)
    resultados = [obj for obj in lista if obj[key] in resultados_value]
    
    return resultados
  
  def moreSimilarWord(self, string_base: str, lista: list, key: str, limite=0.6):     
    similares = []
    for item in lista:
        palavras = re.split(r'[@.\s]+', item[key])
        for palavra in palavras:
          similaridade = self.calcSimilaridade(string_base.lower(), palavra.lower())
          # if palavra.lower() == "rafael":
          #   print(string_base.lower(),palavra.lower(),similaridade)
          if similaridade >= limite:
              similares.append(item)
    return similares