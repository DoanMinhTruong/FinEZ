import numpy as np


def get_log_returns(prices):
    """
    Calculate logarithm returns of the assets.
    :param prices: adjusted closing prices of the assets.
    :return: log returns.
    """
    return np.log(prices / prices.shift(1))


def get_covariance_matrix(prices, trading_days=252):
    """
    Calculate covariance matrix.
    :param prices: adjusted closing prices of the assets.
    :param trading_days: the number of trading days in a year.
    :return: covariance matrix.
    """
    return get_log_returns(prices).cov() * trading_days


def get_correlation_matrix(prices):
    """
    Calculate the correlation matrix.
    :param prices: adjusted closing prices of the assets.
    :return: the correlation matrix
    """
    return get_log_returns(prices).corr()


def portfolio_variance(prices, weights):
    """
    The variance of portfolio.
    :param prices: adjusted closing prices of the assets.
    :param weights: weights of the portfolio.
    :return: variance
    """
    cov_matrix = get_covariance_matrix(prices)

    return np.dot(weights.T, np.dot(cov_matrix, weights))


def sharpe_ratio(p_returns, p_volatility, risk_free_rate=0.0436):
    """
    Calculate the Sharpe ratio.
    :param p_returns: expected returns.
    :param p_volatility: volatility
    :param risk_free_rate: risk-free rate of return (GT10:GOV 3.4%).
    :return: Sharpe ratio.
    """
    sharpe = []
    for ret in p_returns:
        sharpe.append((ret - risk_free_rate) / p_volatility[p_returns.index(ret)])
    return sharpe




