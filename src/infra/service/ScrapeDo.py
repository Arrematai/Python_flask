import requests
import urllib.parse
from dotenv import load_dotenv
import os
load_dotenv()

def ScrapeDo(method, url,body,header):
  token = os.getenv("PROXY_API_KEY_SCRAPEDO")
  geoCode = "br"
  targetUrl = urllib.parse.quote(url, safe='')
  urlFormat = f"https://api.scrape.do?token={token}&URL={targetUrl}"
  
  print(targetUrl)
  print(urlFormat)
  
  if(method == "GET"):
    response = requests.get(urlFormat, params=body, headers=header, timeout=20)
  else:
    response = requests.request(method, urlFormat, headers=header, data=body, timeout=20)
  
  return response
