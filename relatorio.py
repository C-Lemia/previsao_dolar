import pandas as pd
from fpdf import FPDF
import os


def salvar_relatorio_csv(df, previsao, caminho="relatorios/relatorio_dolar.csv"):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    nova_linha = df.iloc[-1].copy()
    nova_linha["venda_amanha"] = previsao
    nova_linha["observacao"] = "Previsão para amanhã"

    df_completo = pd.concat(
        [df, pd.DataFrame([nova_linha])], ignore_index=True)
    df_completo.to_csv(caminho, index=False)
    print(f"Relatório CSV salvo em: {caminho}")


def gerar_relatorio_pdf(df, previsao, caminho="relatorios/relatorio_dolar.pdf"):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Previsão do Dólar", ln=True, align='C')
    pdf.ln(10)

    # Últimos dados
    ultima_data = df.index[-1]
    ultima_venda = df["venda"].iloc[-1]

    pdf.cell(200, 10, txt=f"Última data: {ultima_data}", ln=True)
    pdf.cell(200, 10, txt=f"Valor de venda: R$ {ultima_venda:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Previsão para amanhã: R$ {previsao:.4f}", ln=True)

    pdf.output(caminho)
    print(f"Relatório PDF salvo em: {caminho}")
