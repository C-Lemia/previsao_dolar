import requests
import pandas as pd  #---------- IMPORTAÇÃO DE BIBLIOTECAS

def coletar_cotacoes_usd_brl(dias=60):#---------- FUNÇÃO PARA COLETAR COTAÇÕES USD/BRL
    url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{dias}"  
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erro na requisição: {response.status_code}")

    data = response.json()
    df = pd.DataFrame(data)
    df = df[["timestamp", "bid", "ask"]].copy()
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df = df.rename(columns={
        "timestamp": "data",
        "bid": "compra",
        "ask": "venda"
    })
    df = df.sort_values("data").reset_index(drop=True)
    return df


def coletar_moedas_comparativas():#---------- FUNÇÃO PARA COLETAR MOEDAS COMPARATIVAS (EX: EUR, BTC)
    moedas = ["EUR-BRL", "BTC-BRL"]
    comparativos = {}

    for moeda in moedas: 
        url = f"https://economia.awesomeapi.com.br/json/daily/{moeda}/60"
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(pd.to_numeric(
            df["timestamp"], errors="coerce"), unit="s")
        df = df.sort_values("timestamp")
        nome = moeda.split("-")[0]
        df = df.rename(columns={"ask": nome})
        comparativos[nome] = df.set_index("timestamp")

    return comparativos
