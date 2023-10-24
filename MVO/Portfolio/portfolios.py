import sys
from Portfolio.calculation_with_prices import *
from Portfolio import capm
import numpy as np


def random_weights(prices, trading_days=252, num_portfolios=10000):
    """
    Generate the random weights for the portfolio.
    :param prices: adjusted closing prices of the assets.
    :param trading_days: the number of trading days in a year.
    :param num_portfolios: number of observation.
    :return: weights, returns and volatility
    """
    p_weights = []
    p_returns = []
    p_volatility = []

    num_assets = len(prices.columns[:-1])  # without market index.
    assets = prices.loc[:, prices.columns != prices.columns[-1]]
    expected_returns = capm.expected_returns(prices)[:-1]
    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights / np.sum(weights)
        p_weights.append(weights)
        p_returns.append(np.dot(weights, expected_returns))
        p_volatility.append(np.sqrt(portfolio_variance(assets, weights)) * np.sqrt(trading_days))

    return p_weights, p_returns, p_volatility


# def _random_sum(n, m):
#     # generate M-1 random numbers between 0 and N
#     nums = np.sort(np.random.uniform(0, n, m-1))
#     # calculate the differences between adjacent numbers
#     diffs = np.diff(np.concatenate(([0], nums, [n])))
#     # return the list of numbers
#     return diffs


# def capital_market_line(prices, risk_free_rate=0.034, trading_days=252):
#     # p_weights_free = []
#     p_weights = []
#     p_returns = []
#     p_volatility = []
#
#     num_assets = len(prices.columns[:-1])
#     assets = prices.loc[:, prices.columns != prices.columns[-1]]
#     expected_returns = capm.expected_returns(prices)[:-1]
#     weights_rf = np.arange(0, 1, 0.0001)
#     for weight_rf in weights_rf:
#
#         weights = _random_sum(1-weight_rf, num_assets)
#         p_weights.append(weight_rf)
#         p_weights.append(weights)
#         p_returns.append(weight_rf*risk_free_rate + np.dot(weights, expected_returns))
#         p_volatility.append(np.sqrt(portfolio_variance(assets, weights)) * np.sqrt(trading_days))
#
#     return p_weights, p_returns, p_volatility


def solve_func(vol, ret, risk_free_rate=0.0436):
    return (ret - risk_free_rate) / vol


def cml(p_weights, p_returns, p_volatility, risk_free_rate=0.0436):
    _, ret, vol = max_sharpe(p_weights, p_returns, p_volatility)
    a = solve_func(vol, ret, risk_free_rate)
    x = np.linspace(0, np.max(p_volatility), 100)
    y = a * x + risk_free_rate
    return x, y


# def efficient_frontier(p_weights, p_returns, p_volatility):
#     w_min, r_min, v_min = min_volatility(p_weights, p_returns, p_volatility)
#     p_returns.sort()
#     efficient_returns = p_returns[p_returns.index(r_min):]
#     return

def min_volatility(p_weights, p_returns, p_volatility):
    """
    Get the weights make minimum volatility.
    :param p_weights: weights
    :param p_returns: returns
    :param p_volatility: volatility
    :return: weight, return, volatility
    """
    min_vol = min(p_volatility)
    index = p_volatility.index(min_vol)
    return p_weights[index], p_returns[index], p_volatility[index]


def max_sharpe(p_weights, p_returns, p_volatility):
    """
    Get the weights make Maximum Sharpe ratio.
    :param p_weights: weights
    :param p_returns: returns
    :param p_volatility: volatility
    :return: weight, return, volatility
    """
    sharpe = sharpe_ratio(p_returns, p_volatility)
    max_ratio = max(sharpe)
    index = sharpe.index(max_ratio)
    return p_weights[index], p_returns[index], p_volatility[index]
