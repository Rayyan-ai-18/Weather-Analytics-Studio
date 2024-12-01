import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_data():
    np.random.seed(42)
    years = np.arange(1920, 2022)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    base_temps = {
        'Jan': 20, 'Feb': 22, 'Mar': 25, 'Apr': 28,
        'May': 32, 'Jun': 30, 'Jul': 28, 'Aug': 27,
        'Sep': 26, 'Oct': 24, 'Nov': 22, 'Dec': 20
    }

    data = {'Year': years}
    for month in months:
        data[month] = base_temps[month] + np.linspace(0, 1.5, len(years)) + \
                      np.random.normal(0, 1.5, len(years))

    return pd.DataFrame(data)

def perform_eda(df):
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    df.boxplot(column=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.title('Temperature Box Plot')
    plt.ylabel('Temperature (°C)')

    plt.subplot(2, 2, 2)
    plt.scatter(df['Year'], df['Jan'], alpha=0.7)
    plt.title('January Temperature Trend')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')

    plt.subplot(2, 2, 3)
    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        plt.plot(df['Year'], df[month], label=month)
    plt.title('Monthly Temperature Trends')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.subplot(2, 2, 4)
    corr_matrix = df[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Monthly Temperature Correlation')

    plt.tight_layout()
    plt.show()

def time_series_analysis(df):
    def adf_test(series):
        result = adfuller(series)
        print(f'ADF Statistic: {result[0]}')
        print(f'p-value: {result[1]}')
        print('Critical Values:')
        for key, value in result[4].items():
            print(f'\t{key}: {value}')

    print("Stationarity Test for January Temperatures:")
    adf_test(df['Jan'])

    rolling_mean = df['Jan'].rolling(window=10).mean()
    rolling_std = df['Jan'].rolling(window=10).std()

    plt.figure(figsize=(12, 6))
    plt.plot(df['Year'], df['Jan'], label='Original')
    plt.plot(df['Year'], rolling_mean, label='Rolling Mean')
    plt.plot(df['Year'], rolling_std, label='Rolling Std')
    plt.title('January Temperature: Rolling Statistics')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.show()

def arima_forecast(df):
    data = df['Jan']

    model = ARIMA(data, order=(1,1,1))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=20)
    forecast_index = pd.date_range(start=str(df['Year'].max()+1), periods=20, freq='Y')

    plt.figure(figsize=(12, 6))
    plt.plot(df['Year'], data, label='Historical Data')
    plt.plot(forecast_index, forecast, color='red', label='Forecast')
    plt.title('ARIMA Forecast for January Temperatures')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.show()

def main():
    df = load_and_preprocess_data()
    perform_eda(df)
    time_series_analysis(df)
    arima_forecast(df)

if __name__ == '__main__':
    main()
