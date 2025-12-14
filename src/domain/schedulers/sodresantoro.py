# import logging
from datetime import datetime
import os
import sys
import subprocess
import json
import time
from typing import Text
# import requests
import uuid

from playwright.sync_api import sync_playwright

from src.domain.schedulers.sincronizar import sincronizar
from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log
from src.domain.schedulers.repository.schedulersLogRepository import SchedulersLogRepository
from src.domain.lotes.repository import LotesRepository


class SchedulerSodreSantoro:
    url: Text = "https://www.sodresantoro.com.br/api/search-lots"
    payload: Text
    headers: Text
    
    def __init__(self, scheduler: str, schedulerLogRepository: SchedulersLogRepository, lotesRepository: LotesRepository):
        self.scheduler = scheduler
        self.schedulerLogRepository = schedulerLogRepository
        self.lotesRepository = lotesRepository
        self.size = 9999
        self.resultados = []
        self.initValue()
        self.log = Log("")
    
    def initValue(self):
        self.payload = {
                "indices": [
                    "veiculos",
                    "judiciais-veiculos"
                ],
                "query": {
                    "bool": {
                        "filter": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "auction_status": "online"
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "auction_status": "aberto"
                                                        }
                                                    }
                                                ],
                                                "must_not": [
                                                    {
                                                        "terms": {
                                                            "lot_status_id": [
                                                                5,
                                                                7
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "auction_status": "encerrado"
                                                        }
                                                    },
                                                    {
                                                        "terms": {
                                                            "lot_status_id": [
                                                                6
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "bool": {
                                                "must_not": {
                                                    "term": {
                                                        "lot_status_id": 6
                                                    }
                                                }
                                            }
                                        },
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "lot_status_id": 6
                                                        }
                                                    },
                                                    {
                                                        "term": {
                                                            "segment_id": 1
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "bool": {
                                                "must_not": [
                                                    {
                                                        "term": {
                                                            "lot_test": True
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            }
                        ]
                    }
                },
                "from": 0,
                "size": self.size,
                "aggs": {
                    "lot_financeable": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_financeable": {
                                "terms": {
                                    "field": "lot_financeable",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_category": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_category": {
                                "terms": {
                                    "field": "lot_category",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_origin": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_origin": {
                                "terms": {
                                    "field": "lot_origin",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_sinister": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_sinister": {
                                "terms": {
                                    "field": "lot_sinister",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_brand": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_brand": {
                                "terms": {
                                    "field": "lot_brand",
                                    "size": 500,
                                    "order": {
                                        "_key": "asc"
                                    }
                                },
                                "aggs": {
                                    "lot_model": {
                                        "terms": {
                                            "field": "lot_model",
                                            "size": 1500,
                                            "order": {
                                                "_key": "asc"
                                            },
                                            "min_doc_count": 1
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "client_name": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "client_name": {
                                "terms": {
                                    "field": "client_name",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_year_model": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_year_model": {
                                "stats": {
                                    "field": "lot_year_model"
                                }
                            }
                        }
                    },
                    "lot_km": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_km": {
                                "stats": {
                                    "field": "lot_km"
                                }
                            }
                        }
                    },
                    "lot_fuel": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_fuel": {
                                "terms": {
                                    "field": "lot_fuel",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_transmission": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_transmission": {
                                "terms": {
                                    "field": "lot_transmission",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_optionals": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_optionals": {
                                "terms": {
                                    "field": "lot_optionals",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_location": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_location": {
                                "terms": {
                                    "field": "lot_location",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_praca_label": {
                        "filter": {
                            "bool": {
                                "must": []
                            }
                        },
                        "aggs": {
                            "lot_praca_label": {
                                "terms": {
                                    "field": "lot_praca_label",
                                    "size": 100,
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "min_doc_count": 0
                                }
                            }
                        }
                    }
                },
                "sort": [
                    {
                        "lot_status_id_order": {
                            "order": "asc"
                        }
                    },
                    {
                        "auction_date_init": {
                            "order": "asc"
                        }
                    }
                ]
            }

    def run(self, headless):
        with sync_playwright() as p:
            # 🚀 Inicia navegador com perfil persistente
            context = p.chromium.launch_persistent_context(
                user_data_dir="/tmp/playwright-sodre",
                headless=headless,  # ⚠️ Cloudflare precisa do modo visível
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--window-position=-32000,-32000",  # esconde janela
                ],
            )

            page = context.new_page()

            # 🕵️ Disfarça automação
            page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt']});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            """)

            print("🌐 Acessando Sodré Santoro...")
            page.goto("https://www.sodresantoro.com.br/veiculos", timeout=90000)
            page.wait_for_load_state("networkidle")


            # 📡 Faz a requisição real
            print("📡 Enviando requisição para /api/search-lots...")
            response = context.request.post(
                "https://www.sodresantoro.com.br/api/search-lots",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Origin": "https://www.sodresantoro.com.br",
                    "Referer": "https://www.sodresantoro.com.br/veiculos",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/142.0.0.0 Safari/537.36",
                    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                },
                data=json.dumps(self.payload),
            )

            print("🔎 Status:", response.status)
            if response.status == 200:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            else:
                print("❌ Erro:", response.text())

            context.close()
            return response
        
                
    def exec(self):
        print("INICIADO SCHEDULER SODRE", datetime.now())
        response = None
        display = os.environ.get("DISPLAY")
        if not display:
            print("🖥️ Nenhum display detectado. Iniciando via xvfb-run...")
            cmd = None

            if os.name == "nt":  # Windows
                print("➡️ Ambiente Windows detectado (xvfb não é necessário).")
                cmd = ["python", "src/infra/service/PlayWright.py", "0", "9999"]
            else:  # Linux
                print("➡️ Iniciando via xvfb-run...")
                cmd = ["xvfb-run", "-a", "python3", "src/infra/service/PlayWright.py", "0", "9999"]
                
            # roda xvfb-run e espera terminar
            result = subprocess.run(cmd, capture_output=True, text=True)
            # print("📤 Saída:")
            # print(result)
            if result.stderr.strip():
                print("⚠️ Erro:")
                print(result.stderr)


            response = json.loads(result.stdout)
            
        
        else:
            print(f"✅ Display detectado: {display}")
            response = self.run(headless=False)
            
        
        for item in response["results"]:
        
            lote = item["lot_id"] 
            valor_atual = item["bid_actual"] or None
            tipo_veiculo = item["lot_category"] or None
            marca = item["lot_brand"] or None
            modelo = item["lot_title"] or None
            descricao = item["lot_description"] or None
            data_leilao = item["auction_date_init"] or None
            data_leilao_final = item["lot_date_end"] or None
            cor = item.get("lot_color", None)
            combustivel = item.get("lot_fuel", None)
            kilometragem = item["lot_km"] or None
            transmissao = item["lot_transmission"] or None
            monta = getMonta(item["lot_sinister"]) or None
            ano = f'{item["lot_year_manufacture"]}/{item["lot_year_model"]}'
            thumb = item["lot_pictures"][0] if item["lot_pictures"] else None
            link = f"https://leilao.sodresantoro.com.br/leilao/{item['auction_id']}/lote/{item['lot_id']}/"
            
            agora = datetime.now()
            data_leilao_final_dt = datetime.strptime(data_leilao_final, "%Y-%m-%d %H:%M:%S")
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "descricao": descricao,
                "lote": lote,
                "data_leilao": data_leilao,
                "data_leilao_final": data_leilao_final,
                "marca": marca,
                "modelo": modelo,
                "ano": ano,
                "valor_atual":  valor_atual,
                "tipo_veiculo": tipo_veiculo,
                "monta": monta,
                "thumb": thumb,
                "link": link,
                "cor": cor,
                "combustivel": combustivel,
                "kilometragem": kilometragem,
                "transmissao": transmissao,
                "leiloeiro":"Sodré Santoro",
                "api":self.scheduler,
                "ativo": 1 if data_leilao_final_dt >= agora else 0,

            }# Adiciona o dicionário à lista de resultados
            self.resultados.append(resultado)

        dbLotes = self.lotesRepository.getLotesByApi(self.scheduler)
        inserir,atualizar, remover = sincronizar(dbLotes, self.resultados)

        print("Insert: ",len(inserir))
        print("Updates: ",len(atualizar))
        print("Desativados: ", len(remover))
        
        if len(inserir) > 0:
            for lote in inserir:
                self.lotesRepository.insertLote(lote)

        if len(atualizar) > 0:
            for lote in atualizar:
                lote["updated_at"] = datetime.now()
                lote["ativo"] = 1
                self.lotesRepository.updateLote(lote)

        if len(remover) > 0:
            for lote in remover:
                self.lotesRepository.updateLote({
                'id': lote.get("id"),
                'ativo': 0,
                "updated_at": datetime.now(),
                })
        

        self.schedulerLogRepository.insertLog({ 
            "nome": self.scheduler,
            'status': 'success',
            "duration": 0,
            "results": len(self.resultados)
        })
        print("FINALIZADO SCHEDULER SODRE")
