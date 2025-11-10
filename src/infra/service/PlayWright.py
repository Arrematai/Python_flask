import os
import sys
import subprocess
import json
import time

from playwright.sync_api import sync_playwright

def run(headless, query, size):
    payload = {
                "indices": [
                    "veiculos",
                    "judiciais-veiculos"
                ],
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase_prefix": {
                                    "search_terms": query
                                }
                            }
                        ],
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
                "size": size,
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

        # print("🌐 Acessando Sodré Santoro...")
        page.goto("https://www.sodresantoro.com.br/veiculos", timeout=90000)
        page.wait_for_load_state("networkidle")


        # 📡 Faz a requisição real
        # print("📡 Enviando requisição para /api/search-lots...")
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
            data=json.dumps(payload),
        )
        

        # print("🔎 Status:", response.status)
        if response.status == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            # return response
        else:
            print("❌ Erro:", response.text())
            # return None
            
        context.close()
            
if __name__ == "__main__":
    args = sys.argv
    run(False,args[1], args[2]) 