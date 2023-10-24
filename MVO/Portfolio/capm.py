import sys
from Portfolio.calculation_with_prices import *


def expected_returns(prices, risk_free_rate=0.0436, trading_days=252):
    """
    Compute expected return using Capital Asset Pricing Model.
    :param prices: adjusted closing prices of the assets,
    market index (VNINDEX).
    :param risk_free_rate: risk-free rate of return
    :param trading_days: the number of trading days in a year.
    :return: annualised return estimate.
    """
    market_portfolio = prices.columns[-1] # VNINDEX
    log_returns = get_log_returns(prices)
    cov_matrix = get_covariance_matrix(prices, trading_days)
    betas = cov_matrix[market_portfolio] / cov_matrix.loc[market_portfolio, market_portfolio]
    # betas = betas.drop(market_portfolio)
    market_mean_return = log_returns[market_portfolio].mean() * trading_days
    return risk_free_rate + betas * (market_mean_return - risk_free_rate)
