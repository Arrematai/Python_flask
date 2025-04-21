from scrapfly import ScrapflyClient, ScrapeConfig, ScrapeApiResponse
from dotenv import load_dotenv
import os
load_dotenv()



def ScrapflyScrape(method, url,body,header) :
  scrapfly = ScrapflyClient(key=os.getenv("PROXY_API_KEY_SCRAPFLY"))
  response = scrapfly.scrape(ScrapeConfig(
            tags=[
            "player","project:default"
            ],
            country="br",
            asp=True,
            url=url,
            body=body,
            method=method,
            headers=header
        ))
  
  return response