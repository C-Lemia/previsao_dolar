import os
import pandas as pd
import matplotlib.pyplot as plt
from coletar_dados import coletar_cotacoes_usd_brl
from transformar_dados import transformar_dados
from modelar_previsao import prever_dolar
from relatorio import salvar_relatorio_csv, gerar_relatorio_pdf
from coletar_dados import coletar_moedas_comparativas


import matplotlib
matplotlib.use('Agg') #------- PARA AMBIENTES SEM GUI

def main():
    print("Coletando dados da API...")
    df_raw = coletar_cotacoes_usd_brl(dias=60)

    print("Transformando dados...")
    df = transformar_dados(df_raw)

    print("Modelando previsão...")
    forecast_df = prever_dolar(df)

    print("Previsão gerada:")
    print(forecast_df.tail())

    os.makedirs("output", exist_ok=True)

    # ----- SALVAR CSV
    forecast_df.to_csv("output/previsao_usdbrl.csv", index=False)

    # ----- GRAFICOS 
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['venda'], label='Histórico', color='gray')
    plt.plot(df.index, df['media_movel_5d'],
             label='Média Móvel 5d', linestyle='--')
    plt.plot(df.index, df['media_movel_10d'],
             label='Média Móvel 10d', linestyle='--')
    plt.plot(forecast_df['ds'], forecast_df['yhat'],
             label='Previsão', color='blue')
    plt.fill_between(forecast_df['ds'], forecast_df['yhat_lower'], forecast_df['yhat_upper'],
                     color='blue', alpha=0.2, label='Incerteza')
    plt.title("Previsão da Cotação USD/BRL com Médias Móveis")
    plt.xlabel("Data")
    plt.ylabel("Cotação (R$)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/grafico_previsao_completo.png")

    # ---- HISTOGRAMA
    df['variacao_diaria'] = df['venda'].diff()
    plt.figure(figsize=(10, 4))
    plt.hist(df['variacao_diaria'].dropna(), bins=20,
             color='purple', edgecolor='black')
    plt.title("Histograma da Variação Diária do Dólar (R$)")
    plt.xlabel("Variação diária")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.savefig("output/histograma_variacao.png")


    # ---- Dólar x Euro x Bitcoin
    print("Gerando gráfico comparativo com Euro e Bitcoin...")
    comparativos = coletar_moedas_comparativas()
    df_eur = comparativos["EUR"]
    df_btc = comparativos["BTC"]

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['venda'], label="USD/BRL", color='blue')
    plt.plot(df_eur.index, df_eur['EUR'], label="EUR/BRL", color='green')
    plt.plot(df_btc.index, df_btc['BTC'], label="BTC/BRL", color='orange')
    plt.title("Comparativo: USD vs EUR vs BTC (cotação em BRL)")
    plt.xlabel("Data")
    plt.ylabel("Cotação (R$)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/grafico_comparativo_ativos.png")

    # ----- RELATÓRIO
    print("Gerando relatórios...")
    ultima_previsao = forecast_df.iloc[-1]["yhat"]
    salvar_relatorio_csv(df, ultima_previsao)
    gerar_relatorio_pdf(df, ultima_previsao)


if __name__ == "__main__":
    main()
