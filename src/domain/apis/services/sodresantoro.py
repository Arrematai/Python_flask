# import logging
from typing import Text
# import requests
import uuid

from src.infra.service.PlayWright import run_search

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
                "indices": [
                    "veiculos",
                    "judiciais-veiculos"
                ],
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase_prefix": {
                                    "search_terms": self.query
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

        
    def exec(self):
            
        base_list_url = f"https://www.sodresantoro.com.br/atendimento"
        api_url = "https://www.sodresantoro.com.br/api/search-lots"

        data = run_search(query=self.query, size=9999, headless=False,playload=self.payload)


        for item in data["results"]:
            
            lote = item["lot_id"] 
            valor_atual = item["bid_actual"] or None
            tipo_veiculo = item["lot_category"] or None
            marca = item["lot_brand"] or None
            modelo = item["lot_title"] or None
            monta = getMonta(item["lot_sinister"]) or None
            ano = f'{item["lot_year_manufacture"]}/{item["lot_year_model"]}'
            thumb = item["lot_pictures"][0] if item["lot_pictures"] else None,
            link = f"https://leilao.sodresantoro.com.br/leilao/{item['auction_id']}/lote/{item['lot_id']}/",
            
            
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
        return { "resultados": self.resultados, "http_code": 200 }
    
