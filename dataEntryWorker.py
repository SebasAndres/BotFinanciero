import requests as rq
import pandas as pd
import datetime

# Consumo de APIs
def getDolarMepValues() -> tuple:
    try:
        data = rq.get('https://dolarapi.com/v1/dolares/bolsa').json()
        return data['compra'], data['venta']
    except Exception as e:
        raise Exception(f'Error al obtener los valores del dolar MEP: {e}')

# Escritura en BD locales
def addDolarMepRegistry(date, buy, sell):
    data = open("datasources/dolarMEP.csv", "a")
    data.write(f"{date},{buy},{sell}\n")
    data.close() 

def addInflacionMensualRegistry(date, value):
    data = pd.read_csv('datasources/inflacionMensual.csv')
    data = data.append({'Date': date, 'Value': value}, ignore_index=True)
    data.to_csv('inflacionMensual.csv', index=False)

if __name__ == '__main__':
    date = datetime.datetime.now().timestamp()

    # agrego registro del dolar MEP
    MEP_buy, MEP_sell = getDolarMepValues()
    addDolarMepRegistry(date, MEP_buy, MEP_sell)

