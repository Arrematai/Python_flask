from src.infra.database.mysql import DataBase
from src.domain.log.repository import LogsRepository

class CalcController:

   def __init__(self, database: DataBase):
      self.database = database
      self.repositoryLog = LogsRepository(self.database)


   def calcViabilidade(self,dados,ip):
      try:

         self.repositoryLog.insertCalc({
            "ip": ip,
            "uso": dados.get("uso") or None,
            "fipe": dados.get("fipe") or None,
            "monta": dados.get("monta") or None,
            "comissao": dados.get("comissao") or None,
            "despesa": dados.get("despesa") or None,
            "disponivel": dados.get("disponivel") or None,
            "lance_max": dados.get("lance_max") or None,
            'venda': dados.get("venda") or None,
            "lucro": dados.get("lucro") or None
         })
         self.database.close();
         return;
   
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()
  
   def calSimplificado(self, dados):
      try:
        # Desestruturação (extração de campos específicos)
        fipeId = dados.get("fipeId")
        taxa = dados.get("taxa")
        reparos = dados.get("reparos")
        despesas = dados.get("despesas")

        if not fipeId:
           raise Exception("Fipe não enviada.")
        
        if not taxa:
           raise Exception("Valor da taxa não enviada.")
        
        if not reparos:
           raise Exception("Valor do reparo não enviada.")
        
        if not despesas:
           raise Exception("Valor do despesas não enviada.")


        taxa = float(taxa)
        reparos = float(reparos)
        despesas = float(despesas)

        valor = taxa + reparos + despesas

        self.database.connection()
        # Executando uma consulta SELECT
        query = "SELECT id, AnoModelo, CodigoFipe, Combustivel, Marca, marcaId, MesReferencia, Modelo, modeloId, SiglaCombustivel, TipoVeiculo, Valor FROM fipes where id = %s LIMIT 1"
        self.database.socket.execute(query, (fipeId,))

        # Recuperando os resultados
        dados = self.database.socket.fetchone()

        if not dados:
          raise Exception("Fipe não existe.")
      
        return { "valor": valor + float(dados["Valor"].replace("R$", "").replace(".", "").replace(",", ".")) }
            
      except Exception as e:
          print(f"Error: {e}")
          self.database.close()