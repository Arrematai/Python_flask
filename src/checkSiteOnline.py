from src.infra.database.mysql import DataBase
from src.domain.leiloeiros.repository import LeiloeirosRepository

import requests
import cloudscraper

def init():
  print("Inicio Aplicação")
  
  headers= {
      "Connection": "keep-alive",
      "Accept": "*/*",
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
      "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Windows\"",
      "sec-fetch-dest": "document",
      "sec-fetch-mode": "navigate",
      "sec-fetch-site": "same-origin",
      "sec-fetch-user": "?1",
      "upgrade-insecure-requests": "1",
  }
  
  database = DataBase(dictionary=True)
  repository = LeiloeirosRepository(database)

  
  leiloeiros = repository.findLeiloeirosStatusSite(0)

  
  for l in leiloeiros:
    try:
      
      site = f'https://{l["site"]}'
      headers["origin"] = site
      response = requests.get(url=site, headers=headers, timeout=5)
      
      print(l["site"], response.status_code)
      
      if response.status_code >= 200 and response.status_code <= 299:
        repository.updateStatusSite(l["id"], 1)
      else:
        # Cria uma instância do scraper do Cloudflare
        scraper = cloudscraper.create_scraper()
        responseScraper = scraper.get(site)
        print(l["site"], responseScraper.status_code)
        if responseScraper.status_code >= 200 and responseScraper.status_code <= 299:
          repository.updateStatusSite(l["id"], 1)
        else:
          repository.updateStatusSite(l["id"], 0)
        
    except requests.exceptions.RequestException as e:
        repository.updateStatusSite(l["id"], 0)
    except Exception as e:
      print(f"Error: {e}")
    finally: 
      database.conn.close()
  
 

  print("Aplicação Finalizada")