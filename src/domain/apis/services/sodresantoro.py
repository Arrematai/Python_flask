import os
# import logging
from typing import Text
import requests
import uuid

from src.infra.helpers.Monta import getMonta
from src.infra.service.Logging import Log


class ServiceSantoro:
    url: Text = "https://www.sodresantoro.com.br/api/search-lots"
    payload: Text
    headers: Text
    
    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.resultados = []
        self.initValue()
        self.log = Log("")
    
    def initValue(self):
        self.payload = {
            "index": "veiculos",
            "query": {
                "indices_boost": [
                    {"judiciais-veiculos": 3},
                    {"judiciais-imoveis": 3},
                    {"judiciais-materiais": 3}
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"lot_test": False}},
                            {
                                "bool": {
                                    "should": [
                                        {"bool": {"must": [{"term": {"auction_status": "online"}}]}},
                                        {
                                            "bool": {
                                                "must": [{"term": {"auction_status": "aberto"}}],
                                                "must_not": [{"terms": {"lot_status_id": [5, 6, 7]}}]
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "multi_match": {
                                                            "query": self.query,
                                                            "fields": ["lot_description"],
                                                            "type": "bool_prefix"
                                                        }
                                                    },
                                                    {
                                                        "wildcard": {
                                                            "lot_description": {"value": f"*{self.query}*"}
                                                        }
                                                    }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                "sort": [
                    {"lot_status_id_order": {"order": "asc"}},
                    {"auction_date_init": {"order": "asc"}}
                ],
                "from": 0,
                "size": 48,
                "collapse": {
                    "field": "lot_id",
                    "inner_hits": {
                        "name": "unique_lots",
                        "size": 1
                    }
                },
                "aggs": {
                    "lot_financeable": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_financeable": {
                                "terms": {
                                    "field": "lot_financeable",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_category": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_category": {
                                "terms": {
                                    "field": "lot_category",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_origin": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_origin": {
                                "terms": {
                                    "field": "lot_origin",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_sinister": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_sinister": {
                                "terms": {
                                    "field": "lot_sinister",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_brand": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_brand": {
                                "terms": {
                                    "field": "lot_brand",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                },
                                "aggs": {
                                    "lot_model": {
                                        "terms": {
                                            "field": "lot_model",
                                            "size": 200,
                                            "order": {"_key": "asc"},
                                            "min_doc_count": 1
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "client_name": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "client_name": {
                                "terms": {
                                    "field": "client_name",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_year_model": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_year_model": {
                                "stats": {"field": "lot_year_model"}
                            }
                        }
                    },
                    "lot_km": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_km": {
                                "stats": {"field": "lot_km"}
                            }
                        }
                    },
                    "lot_fuel": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_fuel": {
                                "terms": {
                                    "field": "lot_fuel",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_transmission": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_transmission": {
                                "terms": {
                                    "field": "lot_transmission",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_optionals": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_optionals": {
                                "terms": {
                                    "field": "lot_optionals",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_location": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_location": {
                                "terms": {
                                    "field": "lot_location",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    },
                    "lot_praca_label": {
                        "filter": {"bool": {"must": []}},
                        "aggs": {
                            "lot_praca_label": {
                                "terms": {
                                    "field": "lot_praca_label",
                                    "size": 200,
                                    "order": {"_key": "asc"},
                                    "min_doc_count": 0
                                }
                            }
                        }
                    }
                },
                "post_filter": {
                    "bool": {
                        "must": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "multi_match": {
                                                            "query": self.query,
                                                            "fields": ["lot_description"],
                                                            "type": "bool_prefix"
                                                        }
                                                    },
                                                    {
                                                        "wildcard": {
                                                            "lot_description": {"value": f"*{self.query}*"}
                                                        }
                                                    }
                                                ],
                                                "minimum_should_match": 1
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "must_not": []
                    }
                }
            }
        }

        self.headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.sodresantoro.com.br",
            "referer": f"https://www.sodresantoro.com.br/veiculos/lotes?page=1&q={self.query}",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "cookie": f"message-news=opened; _gcl_au=1.1.2026430349.1743375295; __Secure-Spvll=afa408e196515a70c3e287dd91c0cd856006ce7c861f26a12c4761a316c79607.48526b52ad5bf8da5b39dd8b9efbf54e9279e098120ab5d0ec21fd6b3873b118.2273; _hjSessionUser_2868127=eyJpZCI6IjJjOWUzMTczLWY3ZjAtNTRkZS1hMzc0LTI4ZDM3MjAwZjk4NyIsImNyZWF0ZWQiOjE3NDMzNzUyOTYzMjMsImV4aXN0aW5nIjp0cnVlfQ==; LPVID=Y4ZjA3NjU4NjlkZTkzNDQx; _ga=GA1.1.101407952.1743375297; _ga_HCDECGSBK7=GS1.1.1743447102.2.1.1743448385.60.0.0; _hjSession_2868127=eyJpZCI6ImU5Nzg2Y2JlLTRkOGEtNDhjYi04MjU2LTg5NTlhZDI2NzUwMSIsImMiOjE3NDQ5MzEwMTgzMTAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; login-cta=false; az_botm=0906df4b825217fe3d27839b95351f0d; az_asm=qZDWOBlXCasm7hRYYMW3gazt4kLqfAI8T+Nw332jMhCiL/iTyrGT9oK5HLfrp6AmbHhsg7Lat0rIpzUe; _ga_243MMWR5ZK=GS1.1.1744931017.4.1.1744931476.54.0.1914607123",
        }
    def exec(self):
        response = requests.post(self.url, json=self.payload, headers=self.headers)


        if response.status_code != 200:
            print(response.content)
            self.log.messageError(f"Erro em acesso site {self.url}, status code : {response.status_code}")
            return { "resultados": self.resultados, "http_code": response.status_code }

        data = response.json()



        for item in data.get('hits', []):
            
            lote = item.get("lot_id")
            valor_atual = item.get("bid_actual")
            tipo_veiculo = item.get("lot_category")
            marca = item.get("lot_brand")
            modelo = item.get("lot_model")
            monta = getMonta(item.get("lot_sinister"))
            ano = item.get("lot_year_manufacture")
            thumb = item.get("lot_pictures")[0] if item.get("lot_pictures") else None,
            link = f"https://leilao.sodresantoro.com.br/leilao/{item.get('auction_id')}/lote/{item.get('lot_id')}/?ref=v2",
            
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": lote,
                "chassi": None,
                "valor_fipe": None,
                "valor_atual":  valor_atual,
                "tipo_veiculo": tipo_veiculo,
                "marca": marca,
                "modelo": modelo,
                "monta": monta,
                "ano": ano,
                "thumb": thumb,
                "link": link,
                "leiloeiro":"Sodré Santoro",
                "ativo": 1,

            }# Adiciona o dicionário à lista de resultados
            self.resultados.append(resultado)

        # Exibe os resultados
        # print(len(resultados))
        return { "resultados": self.resultados, "http_code": response.status_code }
    
