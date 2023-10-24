import sys
from Portfolio import capm, calculation_with_prices
import numpy as np


def one_asset(prices, trading_days=252):
    expected_returns = capm.expected_returns(prices).tolist()[:-1]
    volatility = []
    num_assets = len(prices.columns[:-1])
    assets = prices.loc[:, prices.columns != prices.columns[-1]]

    matrix = a = np.diag(np.diag(np.ones((num_assets, num_assets))))
    weights = [matrix[i].tolist() for i in range(num_assets)]

    for w in weights:
        volatility.append(
            np.sqrt(calculation_with_prices.portfolio_variance(assets, np.array(w))) * np.sqrt(trading_days)
        )

    return expected_returns, volatility
# tickers = ['AAPL', 'IBM', '^GSPC']
# start_date = "2020-1-1"
# end_date = "2022-12-31"
# data = stock_prices.get_data_from_yfinance(tickers, start_date, end_date)
# prices = data.loc[start_date:end_date]
#
# expected_returns, volatility = one_asset(prices)
# print(expected_returns)
# print(volatility)
# print(prices)
