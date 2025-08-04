import pandas as pd

def transformar_dados(df):
    """
    Transforma os dados brutos de cotação em dados prontos para modelagem preditiva.
    Adiciona médias móveis e transforma datas em índice temporal.
    """
    df["data"] = pd.to_datetime(df["data"])
    df.set_index("data", inplace=True)

    df["compra"] = df["compra"].astype(float)
    df["venda"] = df["venda"].astype(float)

    df["media_movel_5d"] = df["venda"].rolling(window=5).mean()
    df["media_movel_10d"] = df["venda"].rolling(window=10).mean()

    df["venda_amanha"] = df["venda"].shift(-1)

    df.dropna(inplace=True)

    return df
