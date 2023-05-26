import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller


def realizar_prediccion():
    # Cargar datos de producción y convertir el índice a fechas mensuales
    df = pd.read_csv('produccionketchupmensual.csv', parse_dates=['Fecha mensual produccion'],
                     index_col='Fecha mensual produccion')
    df.index.freq = 'MS'

    # Visualizar la serie de tiempo
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['cantidad producida'], label='Cantidad producida')
    plt.plot(df.index, df['cantidad distribuida'], label='Cantidad distribuida')
    plt.title('Producción de Salsa Ketchup KRIS', fontsize=20)
    plt.xlabel('Fecha mensual producción')
    plt.ylabel('Producción unidades')
    plt.legend()
    plt.show()

    # Prueba de Dickey-Fuller aumentada para comprobar si la serie es estacionaria
    result = adfuller(df['cantidad producida'])
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

    # Aplicar diferenciación para estacionarizar la serie
    df_diff = df['cantidad producida'].diff().dropna()

    # Visualizar la serie diferenciada
    plt.figure(figsize=(12, 6))
    plt.plot(df_diff.index, df_diff)
    plt.title('Producción de Salsa Ketchup KRIS - Serie Diferenciada', fontsize=20)
    plt.xlabel('Fecha mensual producción')
    plt.ylabel('Producción unidades')
    plt.show()

    # Prueba de Dickey-Fuller aumentada para comprobar si la serie diferenciada es estacionaria
    result_diff = adfuller(df_diff)
    print('ADF Statistic (diff):', result_diff[0])
    print('p-value (diff):', result_diff[1])
    print('Critical Values (diff):')
    for key, value in result_diff[4].items():
        print('\t%s: %.3f' % (key, value))

    # Función para trazar ACF y PACF
    def plot_acf_pacf(y, lags=12):
        fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        plot_acf(y, lags=lags, ax=ax[0])
        plot_pacf(y, lags=lags, ax=ax[1])
        plt.show()

    # Graficar ACF y PACF de la serie diferenciada
    plot_acf_pacf(df_diff)

    # Dividir los datos en conjunto de entrenamiento y validación
    train_size = int(len(df) * 0.8)
    train_data = df['cantidad producida'][:train_size]
    test_data = df['cantidad producida'][train_size:]

    # Modelar la serie con SARIMAX
    model = SARIMAX(train_data, order=(2, 1, 0), seasonal_order=(0, 1, 1, 12), enforce_stationarity=False,
                    enforce_invertibility=False)
    model_fit = model.fit()

    # Ver el resumen del modelo
    print(model_fit.summary())

    # Hacer predicciones en el conjunto de validación
    predictions = model_fit.predict(start='2022-06-01', end='2023-05-01', dynamic=False)

    # Calcular el error de las predicciones
    error = np.sqrt(np.mean((predictions - test_data) ** 2))

    # Retornar las predicciones y el error
    return predictions, error
