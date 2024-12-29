import os
# import logging
from typing import Text
import requests
import uuid


class ServiceCopart:
    url: Text = 'https://www.copart.com.br/public/lots/search'
    payload: Text
    headers: Text

    def __init__(self, query, size):
        self.query = query
        self.size = size
        self.initValue()
        
    def initValue(self):
        self.payload = f"length={self.size}&search%5Bvalue%5D=&search%5Bregex%5D=false&filter%5Bupcominglots%5D=exclude_upcoming_lots%3A*&query={self.query}&watchListOnly=false&freeFormSearch=true&page=0&size={self.size}"
        self.headers= {
            "cookie": "copartbrmember=00df814ca4b576071d1e8881929849e1",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "visid_incap_1046344=UnXbvuBQTcWGX9QXlhvawTQ9cmYAAAAAQUIPAAAAAABneqsCps9dLCbwqh9Q2UCx; _fbp=fb.2.1718762814309.23790209733670714; tt.u=0100007FD1317266E906033802B9AF11; rdtrk=%7B%22id%22%3A%227c755536-f5cf-434b-a4c2-4cf353b6d28a%22%7D; OAID=e545c6c595a605e76211455399bdf6b1; userCategory=RPU; g2app.username=; _ga=GA1.1.134325795.1718762814; _ga_63JLT6J1TE=deleted; g2app.acceptCookiePolicy=true; copartbrmember=00df814ca4b576071d1e8881929849e1; userLang=pt_BR; nlbi_1046344=dglaJdTHExLmsrrhMphbYQAAAAAkfSnlclBRroFe5eRSxOv4; g1usersessionid=859d302ca4065527a192cb3db8535491; usersessionid=a464acc53ef4b4804afa8864eaa2ad5e; OAGEO=BR%7CMinas+Gerais%7CNazareno%7C37220-000%7C-21.21639%7C-44.61139%7C%7C035%7C%7CConecta+Ltda.%7CDSL; G2MBRJSESSIONID=5739CB681889EF83A479ACFEAC4C5930-n1; C2BID=705069; cmRzdGF0aW9uLXBvcHVwLTY0Mzg1NDQtdmlld2Vk=viewed; incap_ses_987_1046344=Pb8DBaHyE1YJgjhRYYeyDesCMWcAAAAABw5K1O8U0lxNBGq5cKdS9w==; tt_c_vmt=1731265877; tt_c_c=direct; tt_c_s=direct; tt_c_m=direct; tt.nprf=; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Nov+10+2024+16%3A17%3A18+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202403.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&consentId=de1deaf4-debd-43e1-9645-15039e57d959&interactionCount=0&isAnonUser=1; _ttuu.s=1731266240543; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJleHRyYV9wYXJhbXMiOnt9fSwiY3VycmVudF9zZXNzaW9uIjp7InZhbHVlIjoiKG5vbmUpIiwiZXh0cmFfcGFyYW1zIjp7fX0sImNyZWF0ZWRfYXQiOjE3MzEyNjYyNDA1NTF9; _gcl_au=1.1.294617627.1726801367.877339667.1731265261.1731266249; _ga_63JLT6J1TE=GS1.1.1731265260.23.1.1731266711.60.0.1000883153",
            "Origin": "https://www.copart.com.br",
            "Referer": f"https://www.copart.com.br/lotSearchResults/?free=true&query={self.query}&searchCriteria=%7B%22query%22:%5B%22bmw%22%5D,%22watchListOnly%22:false,%22searchName%22:%22%22,%22freeFormSearch%22:true%7D",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-TOKEN": "null"
        }
        
    def exec (self):
        response = requests.post(self.url, data=self.payload, headers=self.headers)
        data = response.json()
        
        resultados = []
        for item in data.get('data', {}).get('results', {}).get('content', []):
            resultado = {
                "uuid": str(uuid.uuid4()),
                "lote": item.get("lotNumberStr"),
                "chassi": item.get("fv"),
                "valor_fipe": item.get("la"),
                "valor_atual": item.get("hb"),
                "tipo_veiculo": item.get("vehicleType"),
                "marca": item.get("mkn"),
                "modelo": item.get("lm"),
                "monta": item.get("damageClassification"),
                "ano": item.get("manufactureYear"),
                "thumb": item.get("tims").replace("thumbnail","vga"),
                "link": "https://www.copart.com.br/lot/" + str(item.get("lotNumberStr")),
                "leiloeiro":"COPART",
                "ativo": 1,
            }
            # Adiciona o dicionário à lista de resultados
            resultados.append(resultado)

        # Exibe os resultados
        print(len(resultados))
        # return jsonify(resultados)
        return resultados
