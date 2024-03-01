import requests as rq
import pandas as pd
import datetime as dt

def getRAVA_access_token():
    # https://api.popupular.io/visitors/ping
    return "38c2d0acd1e574e612d9072481f5df9914d72c29"

def updateDolarMEPRegistry(days=1):
    """
    Actualiza el registro del dolar MEP con el registro de D dias atras
    """
    dt_origin = dt.datetime.now() - dt.timedelta(days=days-1)

    # use RAVA API to get the dolar MEP registry
    url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "es-AR,es;q=0.9,en-GB;q=0.8,en;q=0.7,de-DE;q=0.6,de;q=0.5,es-419;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.rava.com",
        "Referer": "https://www.rava.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "partition": "claromexhomolog",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    data = {
        "access_token": getRAVA_access_token(),
        "especie": "DOLAR MEP",
        "fecha_inicio": dt_origin.strftime("%Y-%m-%d"),
        "fecha_fin": dt.datetime.now().strftime("%Y-%m-%d")
    }
    
    # validate response
    response = rq.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise ValueError(f"Error {response.status_code} al intentar obtener el registro del dolar MEP")    
    response = response.json()['body']

    # update local registry
    mep_ds = open('datasets/rava-dolar-mep-historico.csv', 'a')    
    
    for registry in response:        
        mep_ds.write(','.join([str(v) for k, v in registry.items()]) + "\n")
    mep_ds.close()

if __name__ == '__main__':
    updateDolarMEPRegistry(days=1)
