import os
import pandas as pd
import matplotlib.pyplot as plt
from coletar_dados import coletar_cotacoes_usd_brl
from transformar_dados import transformar_dados
from modelar_previsao import prever_dolar
from relatorio import salvar_relatorio_csv, gerar_relatorio_pdf
from coletar_dados import coletar_moedas_comparativas


import matplotlib
matplotlib.use('Agg')  # ------- PARA AMBIENTES SEM GUI


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
    comparativos = coletar_moedas_comparativas()
    df_eur = comparativos["EUR"]
    df_btc = comparativos["BTC"]

    df_eur['EUR'] = pd.to_numeric(df_eur['EUR'], errors='coerce')
    df_btc['BTC'] = pd.to_numeric(df_btc['BTC'], errors='coerce')

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # ------- (USD e EUR)
    ax1.plot(df.index, df['venda'], label="USD/BRL", color='blue')
    ax1.plot(df_eur.index, df_eur['EUR'], label="EUR/BRL", color='green')
    ax1.set_ylabel("USD/EUR (R$)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_ylim(df['venda'].min() * 0.98, df_eur['EUR'].max()
                 * 1.02)  
    ax1.yaxis.set_major_locator(plt.MaxNLocator(8))

    # ------ (BTC)
    ax2 = ax1.twinx()
    ax2.plot(df_btc.index, df_btc['BTC'], label="BTC/BRL", color='orange')
    ax2.set_ylabel("BTC (R$)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.set_ylim(df_btc['BTC'].min() * 0.95, df_btc['BTC'].max() * 1.05)
    ax2.yaxis.set_major_locator(plt.MaxNLocator(8))

    plt.title("Comparativo: USD vs EUR vs BTC (cotação em BRL)")
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    fig.legend(lines_1 + lines_2, labels_1 + labels_2, loc="lower right")

    fig.tight_layout()
    plt.savefig("output/grafico_comparativo_ativos.png")

    # ----- RELATÓRIO
    print("Gerando relatórios...")
    ultima_previsao = forecast_df.iloc[-1]["yhat"]
    salvar_relatorio_csv(df, ultima_previsao)
    gerar_relatorio_pdf(df, ultima_previsao)


if __name__ == "__main__":
    main()
