import datetime
import uuid
from typing import Text
import requests
import re

from src.infra.helpers.Monta import getMonta
from src.infra.helpers.MarcaCarros import replace_marcas, obter_marcas
from src.infra.service.Logging import Log
from src.infra.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.domain.lotes.repository import LotesRepository

TIPOS_VEICULO = [
    "CARRETA SEMI-REBOQUE",
    "CAMINHONETE",
    "CAMINHAO",
    "CARRO",
    "MOTOCICLETA",
    "ONIBUS",
    "VAN",
    "UTILITARIO",
    "TRATOR",
    "SEMIRREBOQUE",
    "REBOQUE COMUM RANDON SR",
    "REBOQUE COMUM R",
    "REBOQUE COMUM SR",
    "REBOQUE",
    "REBOQUE COMUM",
    "CARRETA",
    "AUTOMOVEL",
    "AUTOMOVEL DE PASSEIO",
    "AUTOMOVEL DE PASSEIO I",
    "CAMIONETA",
    "ONIBUS DE TURISMO",
    "VEICULO",
    "VEICULO I",
    "CAVALO-MECANICO",
]

PALAVRAS_REMOVER = [
    r'RENAVAM[:.\s]*[0-9]+(/[A-Z]{2})?',  # RENAVAM e número
    r'[0-9]{4,30}/[A-Z]{2}',              # números + UF (como 00158559878/SC)
    r'[0-9]{4,30}',                       # números longos (RENAVAM, motor)
    r'\.[0-9]+/[A-Z]{2}',                 # .01154070724/SP
    r'\b(19[8-9][0-9]|20[0-2][0-9]|2030)\b',  # anos de 1980 a 2030
    r'\b(ANO|MARCA|MODELO|CHASSI|CH|NÃO TRANSFERÍVEL|////:)\b',     # palavras
    r'\s{2,}',                            # múltiplos espaços
    r'\bI/?\b',                            # I/ ou I isolado
    r'[\$\%@#¨!,\*]'                       # Caracteres especiais
    r'\bMOTOR\b.*'                        # remove motor de tudo depois
]

class SchedulerReceitaFederal:
    url: Text = "http://www25.receita.fazenda.gov.br/sle-sociedade/api/portal?T=1" 
    parametros: Text
    headers: Text

    def __init__(self, scheduler: str, schedulerLogRepository: SchedulersLogRepository, lotesRepository: LotesRepository ):
        self.scheduler = scheduler
        self.schedulerLogRepository = schedulerLogRepository
        self.lotesRepository = lotesRepository
        self.Marcas = obter_marcas()
        self.resultados = []
        self.editais = []
        self.lotes = []
        self.initValue()
        self.log = Log("")
        
    def initValue(self):
        self.parametros = {
            "T": "2",
        }
        self.headers= {
            'accept': "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
            "x-kl-ajax-request": "Ajax_Request"
        }

    def handleEditais(self, editais):

      if not editais:
         return
      
      if editais:
          
        for edital in editais:
          
          prefixo = edital.get("edle") # 800100/3/2025
          listaLotes =  edital.get("listaLotes")
          data_leilao = edital.get("dataAberturaLances")

          for listaLote in listaLotes:
            lote = listaLote.get("lote")
            ##http://www25.receita.fazenda.gov.br/sle-sociedade/api/lote/800100/3/2025/28
            self.editais.append({
               "url": f"http://www25.receita.fazenda.gov.br/sle-sociedade/api/lote/{prefixo}/{lote}",
               "leilao": prefixo,
               'data_leilao': data_leilao,
               "lote": lote
            })
    
    def _getModelo(self, tipo, lote):
      modelo_match = re.search(rf'{tipo}\s+(.*?)\s+\b(19[8-9][0-9]|20[0-2][0-9]|2030)\b', lote)
      if modelo_match:
          modelo_bruto = modelo_match.group(1)
          modelo_limpo = self.limpar_modelo_marca(modelo_bruto)

          if '/' in modelo_limpo:
            partes = modelo_limpo.split('/', 1)
            return partes[1].strip()
          else:
            partes = modelo_limpo.split(None, 1)
            if len(partes) == 2:
                return partes[1]
            elif len(partes) == 1:
                return None
              
    def _getMarca(self, tipo, lote):
      marca_match = re.search(rf'{tipo}\s+(.*?)\s+\b(19[8-9][0-9]|20[0-2][0-9]|2030)\b', lote)
      if marca_match:
          marca_bruto = marca_match.group(1)
          marca_limpo = self.limpar_modelo_marca(marca_bruto) # divide na primeira ocorrência de espaço

          if '/' in marca_limpo:
            partes = marca_limpo.split('/', 1)
            # return partes[0].strip()
            return replace_marcas(partes[0].strip())
          else:
            partes = marca_limpo.split(None, 1)
            # return partes[0]
            return replace_marcas(partes[0])
    
    def _getAno(self, lote):
      ano_match = re.search(r'\b(19[8-9][0-9]|20[0-2][0-9]|2030)\b', lote)
      if ano_match:
          return int(ano_match.group(1))
      return None
    
    def _getTipo(self, lote):
      texto_maiusculo = lote.upper()
      for tipo in sorted(TIPOS_VEICULO, key=len, reverse=True):
          if tipo in texto_maiusculo:
              return tipo
      return None
    
    def _getChassi(self, lote):
      chassi_match = re.search(r'\b[A-HJ-NPR-Z0-9]{17}\b', lote,flags=re.IGNORECASE)
      if chassi_match:
          return chassi_match.group()
      return None
    
    def _getPlaca(self, lote):
      placa_match = re.search(r'\b[A-Z]{3}-?[0-9][A-Z0-9][0-9]{2}\b', lote,flags=re.IGNORECASE)
      if placa_match:
          return placa_match.group()
      return None
      
    def extrair_tipo(self,texto):
      texto_upper = texto.upper()
      for tipo in TIPOS_VEICULO:
          if tipo in texto_upper:
              return tipo
      return None
  
    def limpar_modelo_marca(self, texto):
      texto_limpo = texto
      for padrao in PALAVRAS_REMOVER:
          texto_limpo = re.sub(padrao, '', texto_limpo,flags=re.IGNORECASE)
      return texto_limpo.strip(" /-.,")
    
    def sincronizar(self, dados_db, dados_novos):

      def chave_composta(item):
        # return (item['lote'], item['leilao'], item["marca"], item["modelo"], item['ano'], item["chassi"])
        return (item['descricao'])

      db_map = {chave_composta(item): item for item in dados_db}
      novos_map = {chave_composta(item): item for item in dados_novos}

      inserir = []
      atualizar = []
      remover = []

      # campos_para_verificar = ['marca', 'modelo', 'ano', 'chassi',"ativo"]
      campos_para_verificar = ['descricao',"ativo"]

      for chave, novo in novos_map.items():
          if chave not in db_map:
              inserir.append(novo)
          else:
            antigo = db_map[chave]
            diff = any(
                novo.get(k) != antigo.get(k)
                for k in campos_para_verificar
            )
            if diff:
                novo["id"] = antigo.get("id")
                novo["uuid"] = antigo.get("uuid")
                atualizar.append(novo)

      for chave, antigo in db_map.items():
          if chave not in novos_map:
              remover.append(antigo)

      return inserir, atualizar, remover

    def exec(self):
      print("INICIADO SCHEDULER RECEITA FEDERAL")

      response = requests.get(self.url, params=self.parametros, headers=self.headers)

      if response.status_code != 200:
          self.log.SchedulerError(self.scheduler, response.status_code)
          self.schedulerLogRepository.insertLog({ 
              "nome": 'receitafederal',
              'status': 'error',
              "duration": 0,
              "results": 0
            })
          return
      
      data = response.json()

      if not data:
          return

      # Crias as URLS de ACESSO
      self.handleEditais(data.get('editais'))
      

      for edital in self.editais:
        try:
          response = requests.get(edital.get("url"))

          if response.status_code != 200: 
            continue
          
          data = response.json()
          lotes = data.get("itensDetalhesLote")
          imagens = data.get("imagens") or []

          for lote in lotes:
            self.lotes.append({
                "leilao": edital.get("leilao"),
                'data_leilao': edital.get("data_leilao"),
                "lote": edital.get("lote"),
                "url": edital.get("url"),
                "descricao": lote.get("descricao"),
                "imagem": f"https://storagegw.estaleiro.serpro.gov.br/sle-pro-publico/arquivos/images/{imagens[0]['src']}" if len(lotes) == 1 and len(imagens) > 0 else None
            })
            

        except Exception as e:
          print(f"Error: {e}")


      for valor in self.lotes:

        lote = valor.get("descricao")
          
        tipo = self._getTipo(lote)
        
        # Caso nao tenha loot
        if not tipo:
          continue

        marca = self._getMarca(tipo,lote)
        modelo = self._getModelo(tipo,lote)

        # Caso nao tenha marca ou modelo
        if not marca or not modelo:
          continue

        ano = self._getAno(lote)
        chassi = self._getChassi(lote)
        placa = self._getPlaca(lote)

  
        resultado = {
          "uuid": str(uuid.uuid4()),
          "descricao": lote,
          "lote": str(valor.get("lote")),
          "leilao": str(valor.get("leilao")),
          'data_leilao': valor.get("data_leilao"),
          "chassi": chassi or None,
          "placa": placa or None,
          "valor_fipe": None,
          "valor_atual": None,
          "tipo_veiculo": tipo,
          "marca": marca,
          "modelo": modelo,
          "monta": getMonta(""),
          "ano": str(ano),
          "thumb": valor.get("imagem"),
          "link": f"http://www25.receita.fazenda.gov.br/sle-sociedade/portal/edital/{valor.get('leilao')}/lote/{valor.get('lote')}",
          "leiloeiro":"Receita Federal",
          "api":"receitafederal",
          "ativo": 1,
        }


        self.resultados.append(resultado)


      dbLotes = self.lotesRepository.getLotesByApi("receitafederal")

      inserir,atualizar, remover = self.sincronizar(dbLotes, self.resultados)

      # print("Insert: ",len(inserir))
      # print("Updates: ",len(atualizar))
      # print("Desativados: ", len(remover))

      
      if len(inserir) > 0:
        for lote in inserir:
          self.lotesRepository.insertLote(lote)

      if len(atualizar) > 0:
        for lote in atualizar:
          lote["updated_at"] = datetime.datetime.now()
          lote["ativo"] = 1
          self.lotesRepository.updateLote(lote)

      if len(remover) > 0:
         for lote in remover:
            self.lotesRepository.updateLote({
               'id': lote.get("id"),
               'ativo': 0,
               "updated_at": datetime.datetime.now(),
            })
      

      self.schedulerLogRepository.insertLog({ 
        "nome": 'receitafederal',
        'status': 'success',
        "duration": 0,
        "results": len(self.resultados)
      })

      # Imprimindo os resultados em formato JSON
      # print(self.resultados)




