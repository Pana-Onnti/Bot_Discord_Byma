import os
import re
import json
import pandas
import requests
import datetime
symbols = []
with open("symbols.txt", "r") as file:
    symbols = [line.strip() for line in file]
   


def fecha(horas):
    hoy = datetime.datetime.now()
    hoy_menos_hora= hoy - datetime.timedelta(hours=horas)
    fecha = hoy_menos_hora.strftime("%Y-%m-%d")
    return fecha

def traer_data (especie,fecha_inicio,fecha_fin):
    #
    #Session  
    s = requests.Session()
    # Funcion para el login
    def strbetw(text, left, right):
      match = re.search( left + '(.*?)' + right, text)
      if match:  
        return match.group(1)
      return ''
    # url y header del login > obtener token  
    url = "https://www.rava.com"
    headers = {
        "Host" : "www.rava.com",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding" : "gzip, deflate, br",    
        "DNT" : "1",
        "Connection" : "keep-alive",      
        "Upgrade-Insecure-Requests" : "1",
        "Sec-Fetch-Dest" : "document",
        "Sec-Fetch-Mode" : "navigate",
        "Sec-Fetch-Site" : "none",
        "Sec-Fetch-User" : "?1"
        }
    response = s.get(url = url, headers = headers)
    status = response.status_code
    if status != 200:
      print("login status", status)  
      exit()
    access_token = strbetw(response.text, ":access_token=\"\'", "\'\"")
    print(access_token)

    #Variables de la peticion
    url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"

    data = {
      "access_token": access_token,  # - Parece que dura 30 minutos 
      "especie": especie,  #Ticker
      "fecha_inicio": fecha_inicio,  #Para que traiga todo
      "fecha_fin": fecha_fin # Para que traiga todo
      }

    headers = {
        "Host" : "clasico.rava.com",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept" : "*/*",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding" : "gzip, deflate",
        "Content-Type" : "application/x-www-form-urlencoded",
        "Origin" : "https://datos.rava.com",
        "DNT" : "1",
        "Connection" : "keep-alive",
        "Referer" : "https://datos.rava.com/",    
        "Sec-Fetch-Dest" : "empty",
        "Sec-Fetch-Mode" : "cors",
        "Sec-Fetch-Site" : "same-site"    
    }
    # Peticion
    response = s.post(url = url, headers = headers, data = data)
    status = response.status_code
    if status != 200:
      print("form status", status)
      exit()
  
    return(pandas.DataFrame(json.loads(response.text)['body']))
