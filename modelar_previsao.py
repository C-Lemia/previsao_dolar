import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import timedelta


def prever_dolar(df, modelo_path="output/modelo_usd.pkl"):
    df_model = df.copy()

    X = df_model[["venda", "media_movel_5d", "media_movel_10d"]]
    y = df_model["venda_amanha"]

    # --- SE O MODELO EXISTE, CARREGA, SE NÃO TREINA E SALVA UM
    if os.path.exists(modelo_path):
        print("Modelo encontrado. Carregando modelo salvo...")
        modelo = joblib.load(modelo_path)
        treinado_novamente = False
    else:
        print("Modelo não encontrado. Treinando novo modelo...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        modelo = LinearRegression()
        modelo.fit(X_train, y_train)
        joblib.dump(modelo, modelo_path)
        treinado_novamente = True

        y_pred = modelo.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print("Avaliação do novo modelo:")
        print(f"R²: {r2:.4f}")
        print(f"MSE: {mse:.4f}")

    # ---- PREVISÃO
    ultima_entrada = df_model[[
        "venda", "media_movel_5d", "media_movel_10d"]].iloc[[-1]]
    previsao = modelo.predict(ultima_entrada)[0]

    data_hoje = df_model.index[-1]
    data_amanha = data_hoje + timedelta(days=1)

    forecast_df = pd.DataFrame({
        "ds": [data_amanha],
        "yhat": [previsao],
        "yhat_lower": [previsao - 0.05],  #------ margem de incerteza ------
        "yhat_upper": [previsao + 0.05]
    })

    return forecast_df
