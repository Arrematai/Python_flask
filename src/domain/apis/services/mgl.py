import json
import uuid
from typing import Text
import requests
import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.infra.helpers.Monta import getMonta



class ServiceMgl:
    url: Text = "https://www.mgl.com.br/ApiFeatures/GetBusca/1/1/0?FiltroCategorias=88&FiltroCategorias=189&FiltroCategorias=108&FiltroCategorias=116&FiltroCategorias=117&FiltroCategorias=204&FiltroCategorias=212&FiltroCategorias=119&FiltroCategorias=169&FiltroCategorias=175&FiltroCategorias=174&FiltroCategorias=173&FiltroCategorias=171&FiltroCategorias=238&FiltroCategorias=180&FiltroCategorias=181&FiltroCategorias=192&FiltroCategorias=170&FiltroCategorias=164"
    parametros: Text
    headers: Text

    def __init__(self, query, size):
        self.HEADLESS = True   
        self.query = query
        self.size = size
        self.initValue()
        self.resultados = []
        
    def initValue(self):
        self.payload = {
                "RangeValores": 0,
                "Scopo": 0,
                "IgnoreScopo": 0,
                "OrientacaoBusca": 0,
                "Mapa": "",
                "Busca": self.query,
                "ID_Categoria": 0,
                "ID_Estado": 0,
                "ID_Cidade": 0,
                "Bairro": "",
                "ID_Regiao": 0,
                "ValorMinSelecionado": 0,
                "ValorMaxSelecionado": 0,
                "CFGs": "[]",
                "Pagina": 1,
                "sInL": "",
                "Ordem": 0,
                "QtdPorPagina": self.size,
                "SubStatus": [],
                "ID_Leiloes_Status": [],
                "PaginaIndex": 1,
                "BuscaProcesso": "",
                "NomesPartes": "",
                "CodLeilao": "",
                "TiposLeiloes": [],
                "PracaAtual": 0,
                "DataAbertura": "",
                "DataEncerramento": "",
                "Filtro": {}
            }
        self.headers= {
            "content-type": "application/json"
        }
        
    
    def _getModelo(self, loteNome:str):
        padrao = re.compile(
            r"""
            ^[^-–]*[-–]+\s*                                # ignora prefixo (cidade e hífen/travessão)
            (?:CARRO|CAMINHONETE|VEÍCULO|VAN|MINIVAN|MICRO-ÔNIBUS|SUCATA|SUCATAS|INSERVÍVEIS|CIRCULÁVEL)?\s*[-/]?\s*  # ignora prefixos
            (?:MODELO\s*)?                                 # ignora "MODELO"
            [A-ZÀ-Ú]{2,}(?:\s*/\s*[A-ZÀ-Ú]+)?\s*           # ignora marca (aceita FIAT / PALIO também)
            (?P<modelo>[A-ZÀ-Ú0-9\s\.–\-]+?)               # captura o modelo base
            (?:[, ]+[A-ZÀ-Ú0-9\s\.–\-]+?)*                 # permite descrições intermediárias (BRANCO, FLEX, CILINDROS)
            (?:[,\.]?\s*(?:ANO\s*)?\d{4}(?:\s*[/,\.]\s*\d{4})?)?  # ignora o ano se houver
            (?:\s*-\s*PA\d+)?                              # ignora códigos tipo - PA12345
            (?:\s*[-–\.]?\s*)?$                            # ignora finais opcionais
            """,
            re.VERBOSE | re.IGNORECASE
        )
        match = padrao.search(loteNome)
        if match:
            modelo = match.group("modelo").strip(" ,.-").title()
            #print(f"✅ Success: {loteNome}")
            return modelo
        else:
            #print(f"⚠️ Error: {loteNome}")
            return None
        
    def _getMarca(self, loteNome:str):
        padrao = re.compile(
            r"""
            ^[^-–]*[-–]+\s*                                # ignora prefixo (cidade e hífen/travessão)
            (?:CARRO|CAMINHONETE|VEÍCULO|VAN|MINIVAN|MICRO-ÔNIBUS|SUCATA|SUCATAS|INSERVÍVEIS|CIRCULÁVEL)?\s*[-/]?\s*  # ignora prefixos
            (?:MODELO\s*)?                                 # ignora "MODELO"
            (?P<marca>[A-ZÀ-Ú]{2,})                        # CAPTURA a marca (ex: FIAT, TOYOTA)
            (?:\s*/\s*[A-ZÀ-Ú]+)?                          # ignora "/" e complementos (FIAT / PALIO)
            """,
            re.VERBOSE | re.IGNORECASE
        )
        match = padrao.search(loteNome)
        if match:
            marca = match.group("marca").strip(" -")
            # print(f"✅ Success: {loteNome}")
            return marca
        else:
            # print(f"⚠️ Error: {loteNome}")
            return None

    def _getAno(self, loteNome:str):
        padrao = re.compile(
            r"""
            (?:[,\.]?\s*(?:ANO\s*)?)           # pode ter a palavra "ANO" ou não
            (?P<ano>\d{4}(?:\s*[/,\.]\s*\d{4})?)   # captura o ano principal (ex: 2019/2020)
            (?![^-]*PA\d+)                    # garante que não faz parte do bloco - PA12345
            """,
            re.VERBOSE | re.IGNORECASE
        )
        match = padrao.search(loteNome)
        if match:
            ano = match.group("ano").strip(" -")
            # print(f"✅ Success: {loteNome} ano {ano}")
            return ano
        else:
            # print(f"⚠️ Error: {loteNome}")
            return None
        

    def _getThumb(self, loteNome:str):
        fotos = loteNome.get("Fotos") or None
        if(len(fotos) > 0):
            return fotos[0]["Foto"]
        else:
            return None
    

    
    
    def exec(self):
        with sync_playwright() as p:
            # print("🚀 Iniciando Chromium...")
            browser = p.chromium.launch(headless=self.HEADLESS)
            context = browser.new_context()

            page = context.new_page()
            # print("🌐 Acessando site principal para obter cookies...")
            page.goto("https://www.mgl.com.br/quem-somos/", timeout=60000)
            page.wait_for_load_state("networkidle")

            # (opcional) definir headers, user-agent, etc. se o site for sensível
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
                "Accept-Language": "pt-BR,pt;q=0.9"
            })

            print("📡 Enviando requisição para API da MGL...")
            result = page.evaluate(
                """async ([payload, url]) => {
                    try {
                        const res = await fetch(url, {
                            method: "POST",
                            headers: {
                                "Accept": "application/json, text/plain, */*",
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify(payload),
                            credentials: "include"
                        });

                        if (!res.ok) {
                            const text = await res.text();
                            throw new Error(`Erro HTTP ${res.status}: ${text}`);
                        }

                        return await res.json();
                    } catch (e) {
                        return { error: e.message };
                    }
                }""",
                [self.payload, self.url]
            )
            
            print(result)
            
            browser.close()
            
            for item in result.get("Lotes") or []:
                loteNome = item.get("Lote")
                modelo = self._getModelo(loteNome) or None
                marca = None
                ano = None
                
                if(modelo):
                    lote = item.get("ID_Leiloes_Lote")
                    marca = self._getMarca(loteNome) or None
                    ano = self._getAno(loteNome) or None
                    thumb = self._getThumb(item) or None
                    link = item.get("URLlote") or None
                    valor_atual = item.get("ValorAvaliacao") or None
                    
                    resultado = {
                        "uuid": str(uuid.uuid4()),
                        "lote": lote,
                        "chassi": None,
                        "valor_fipe": None,
                        "valor_atual":  valor_atual,
                        # "tipo_veiculo": tipo_veiculo,
                        "marca": marca,
                        "modelo": modelo,
                        "monta": getMonta(None),
                        "ano": ano,
                        "thumb": f'https://www.mgl.com.br/imagens-complete/1300x1300/{thumb}',
                        "link": f'https://www.mgl.com.br/{link}',
                        "leiloeiro":"MGL",
                        "ativo": 1,
                    }
                    
                    # Adiciona o dicionário à lista de resultados
                    self.resultados.append(resultado)
                
            
        
        return { "resultados": self.resultados, "http_code": 200 }



