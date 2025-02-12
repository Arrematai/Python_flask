import requests
import time
import cloudscraper
from urllib.parse import urlparse
## INFRA
from src.infra.database.mysql import DataBase
from src.infra.service.Logging import Log

## DOMAIN
from src.domain.leiloeiros.repository import LeiloeirosRepository

# Suppress the warnings from urllib3
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def init():
  log = Log("")
  
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


  leiloeiros = repository.findLeiloeirosStatusSite()

  # leiloeiros = [
  #   {
  #     "id": 21,
  #     "site": "www.andersonoliveira.adm.br"
  #   }
  # ]


  for l in leiloeiros:
    start_time = time.time()  

    site = f'https://{l["site"]}'
    headers["origin"] = site
    try:


      
      response = requests.get(url=site, headers=headers, timeout=10)

      print(site, response.status_code)

      if response.status_code >= 200 and response.status_code <= 299:
        end_time = time.time()
        repository.updateStatusSite(l["id"], 1)
        log.checkOnlineSite(start=start_time,end=end_time,site=site, status=response.status_code)
      else:
        # Cria uma instância do scraper do Cloudflare
        scraper = cloudscraper.create_scraper()
        responseScraper = scraper.get(site)
        print(site, response.status_code)
        if responseScraper.status_code >= 200 and responseScraper.status_code <= 299:
          end_time = time.time()
          repository.updateStatusSite(l["id"], 1)
          log.checkOnlineSite(start=start_time,end=end_time,site=site, status=responseScraper.status_code)
        else:
          end_time = time.time()
          repository.updateStatusSite(l["id"], 0)
          log.checkOnlineSite(start=start_time,end=end_time,site=site, status=responseScraper.status_code)
        
    except requests.exceptions.RequestException as e:
        try:
          response = requests.get(url=site, headers=headers, timeout=10, verify=False)
          print(site, response.status_code)
          if response.status_code >= 200 and response.status_code <= 299:
            end_time = time.time()
            repository.updateStatusSite(l["id"], 1)
            log.checkOnlineSite(start=start_time,end=end_time,site=site, status=response.status_code)
          else:
            end_time = time.time()
            repository.updateStatusSite(l["id"], 0)
            log.checkOnlineSite(start=start_time,end=end_time,site=site, status=response.status_code)
        except Exception as e:
          print(site, 500)
          end_time = time.time()
          repository.updateStatusSite(l["id"], 0)
          log.checkOnlineSite(start=start_time,end=end_time,site=site, status=500)
    except Exception as e:
      print(site, 999)
      end_time = time.time()
      log.checkOnlineSite(start=start_time,end=end_time,site=site, status=999)
      print(f"Error: {e}")

  # Close Connection database
  database.close()
  
 

  print("Aplicação Finalizada")