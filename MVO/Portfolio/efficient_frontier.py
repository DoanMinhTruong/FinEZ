import sys
import numpy as np
import cvxpy as cp
from Portfolio import capm, calculation_with_prices


def efficient_frontier(prices, min_ret, max_ret, trading_days=252):
    expected_returns = capm.expected_returns(prices)
    expected_returns = expected_returns.values[:-1]

    cov_matrix = calculation_with_prices.get_covariance_matrix(prices)
    cov_matrix = cov_matrix.iloc[:-1, :-1].values

    n_assets = len(expected_returns)
    weights = cp.Variable(n_assets)

    # Define the objective function
    objective = cp.Minimize(cp.quad_form(weights, cov_matrix))

    # Define the constraints
    constraints = [cp.sum(weights) == 1, weights >= 0]

    # Define the range of target returns
    target_returns = np.linspace(min_ret, max_ret, num=1000)

    # Calculate the efficient frontier
    efficient_frontier = []
    for r in target_returns:
        constraints.append(weights.T @ expected_returns >= r)
        prob = cp.Problem(objective, constraints)
        prob.solve()
        efficient_frontier.append((r, np.sqrt(prob.value) * np.sqrt(trading_days)))
        constraints.pop()

    return efficient_frontier
