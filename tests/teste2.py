
import json
import time
import argparse
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
from src.infra.service.PlayWright import run_search


#  poetry run teste2 --query "bmw" --page 1 --size 1 --headless false

DEFAULT_PAYLOAD_TEMPLATE = {
    "indices": [
        "veiculos",
        "judiciais-veiculos"
    ],
    "query": {
        "bool": {
            "must": [
                {
                    "match_phrase_prefix": {
                        "search_terms": "fiat"
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
    "size": 48,
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



def build_payload(query,size=20):
    p = DEFAULT_PAYLOAD_TEMPLATE.copy()
    # Deep copy safer for nested structures
    p = json.loads(json.dumps(DEFAULT_PAYLOAD_TEMPLATE))
    p["size"] = size
    return p


def run_search(query: str, size: int = 20, headless: bool = True, retries: int = 2):
    base_list_url = f"https://www.sodresantoro.com.br/veiculos/lotes?term={query}&sort=auction_date_init_asc"
    api_url = "https://www.sodresantoro.com.br/api/search-lots"

    payload = build_payload(query="",size=size)

    # Ajuste: se quiser enviar query string no corpo, pode adaptar aqui.
    # payload["query_string"] = query  # caso necessário

    attempt = 0
    last_error = None

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context()  # cria contexto limpo (cookies isolados)
        page = context.new_page()

        try:
            # Acesse a página de listagem para que os cookies/JS carreguem
            print(f"[+] Navigating to {base_list_url} to initialize session...")
            page.goto(base_list_url, timeout=30000)
            # Espera um pouco para o JS estabelecer cookies/tokens; ajuste se necessário
            page.wait_for_timeout(2000)

            # opcional: aceitar popups/consent banners (exemplo genérico)
            # tentar clicar em botões comuns (não garantido em todo site)
            try:
                page.locator("button:has-text('Aceitar'), button:has-text('Aceito'), button:has-text('OK')").first.click(timeout=1000)
                print("[*] Possible cookie banner closed")
            except Exception:
                pass

            while attempt <= retries:
                attempt += 1
                print(f"[+] Attempt {attempt} to fetch API inside page context...")

                try:
                    # Executa fetch dentro do navegador (herda cookies e contexto)
                    result = page.evaluate(
                        """async ({api_url, payload}) => {
                            try {
                                const res = await fetch(api_url, {
                                    method: "POST",
                                    headers: {
                                        "accept": "application/json, text/plain, */*",
                                        "content-type": "application/json",
                                        // note: não setamos cookies aqui — o browser já envia
                                    },
                                    body: JSON.stringify(payload),
                                    credentials: 'include',
                                });
                                const text = await res.text();
                                let json = null;
                                try {
                                    json = JSON.parse(text);
                                } catch(e) {
                                    // pode não ser JSON
                                    return { ok: false, status: res.status, text };
                                }
                                return { ok: true, status: res.status, json };
                            } catch (err) {
                                return { ok: false, error: String(err) };
                            }
                        }""",
                        {"api_url": api_url, "payload": payload},
                    )

                    if not isinstance(result, dict):
                        last_error = f"Unexpected result type: {type(result)}"
                        print("[-]", last_error)
                        time.sleep(2)
                        continue

                    if result.get("ok"):
                        status = result.get("status")
                        data = result.get("json")
                        print(f"[+] API returned status {status}.")
                        if data:
                            return data
                        # resumir e sair
                        total_hits = None
                        try:
                            # estrutura pode variar, tentamos encontrar total hits
                            if isinstance(data, dict):
                                if "hits" in data and isinstance(data["hits"], dict):
                                    total_hits = data["hits"].get("total")
                                elif "total" in data:
                                    total_hits = data.get("total")
                        except Exception:
                            total_hits = None
                        print(f"[+] Total hits (possible): {total_hits}")
                        browser.close()
                        return data
                    else:
                        # resultado de erro (resposta não JSON ou status != 200)
                        last_error = result
                        print("[-] Fetch returned not ok:", result)
                        # aguardar backoff e tentar novamente
                        time.sleep(2 ** attempt)
                except PWTimeoutError as e:
                    last_error = e
                    print("[-] Playwright timeout:", str(e))
                    time.sleep(2 ** attempt)
                except Exception as e:
                    last_error = e
                    print("[-] Unexpected error:", str(e))
                    time.sleep(2 ** attempt)

            browser.close()
            raise RuntimeError(f"Failed to fetch API after {retries+1} attempts. Last error: {last_error}")
        finally:
            context.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", type=str, default="", help="Texto de busca (q)")
    parser.add_argument("--page", "-p", type=int, default=1, help="Página de listagem")
    parser.add_argument("--size", "-s", type=int, default=20, help="Tamanho (size) do payload")
    parser.add_argument("--headless", type=str, default="true", help="true/false")
    parser.add_argument("--out", type=str, default="sodre_result.json", help="Arquivo de saída JSON")
    parser.add_argument("--retries", type=int, default=2, help="Número de tentativas")
    return parser.parse_args()


def init():
    args = parse_args()
    headless_flag = args.headless.lower() in ("1", "true", "yes", "y")
    print(vars(args))
    data = run_search(query=args.query, size=args.size, headless=headless_flag, retries=args.retries)
    print("[+] Done")
    print(data)
    
    
if __name__ == "__main__":
  init()