from scrapingbee import ScrapingBeeClient
from dotenv import load_dotenv
import os
load_dotenv()



def ScrapingbeeScrape(method, url,body,header):
  client = ScrapingBeeClient(os.getenv("PROXY_API_KEY_SCRAPINGBEE"))
  response = ""

  if method == "GET":
    response = client.get(
      url=url,
      headers=header,
      params={
        'render_js': False,
      }
    )
  elif method == "POST":
    response = client.post(
      url=url,
      headers=header,
      data=body,
      params={
        'render_js': False,
        'premium_proxy': True,
        'country_code': 'br',
      }
    )

  return response