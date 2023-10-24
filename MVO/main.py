from flask import Flask, jsonify, request, Response
from get_data import *
app = Flask(__name__)
from Portfolio import capm, efficient_frontier, calculation_with_prices, portfolios, portfolio_for_one_asset
import json
import numpy as np
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
@app.route('/mvo')
def mvo():
    r = (request.json)
    tickers=r['tickers']
    start_date=r['start_date']
    end_date=r['end_date']
    prices = get_data(tickers, start_date , end_date)
    
    expected_returns, volatility = portfolio_for_one_asset.one_asset(prices)
    p_weights, p_returns, p_volatility = portfolios.random_weights(prices, num_portfolios=3000)
    
    
    w_min, r_min, v_min = portfolios.min_volatility(p_weights, p_returns, p_volatility)
    w_max, r_max, v_max = portfolios.max_sharpe(p_weights, p_returns, p_volatility)
    cml_x, cml_y = portfolios.cml(p_weights, p_returns, p_volatility)
    sharpe_ratio = portfolios.sharpe_ratio(p_returns, p_volatility)
    ef = efficient_frontier.efficient_frontier(prices, r_min, max(expected_returns))
    x_ef = [point[1] for point in ef]
    y_ef = [point[0] for point in ef]

    corr_matrix = calculation_with_prices.get_correlation_matrix(prices).round(3)


    # res['stock_prices'] = prices.to_json(orient="columns")
    res = {
        'prices' : prices.to_json(),
        'p_weights' : json.dumps(p_weights, cls=NumpyEncoder),
        'p_returns' : json.dumps(p_returns, cls=NumpyEncoder), 
        'p_volatility' : json.dumps(p_volatility, cls=NumpyEncoder), 
        'expected_returns' : json.dumps(expected_returns, cls=NumpyEncoder), 
        'volatility' : json.dumps(volatility, cls=NumpyEncoder),
        'sharpe_ratio' : json.dumps(sharpe_ratio, cls=NumpyEncoder),
        'x_ef': json.dumps(x_ef, cls=NumpyEncoder),
        'y_ef': json.dumps(y_ef, cls=NumpyEncoder),
        'cml_x' : json.dumps(cml_x, cls=NumpyEncoder),
        'cml_y' : json.dumps(cml_y, cls=NumpyEncoder),
        'v_min' : json.dumps(v_min, cls=NumpyEncoder),
        'v_max' : json.dumps(v_max, cls=NumpyEncoder),
        'corr_matrix' : corr_matrix.to_dict(orient='records'),
        'w_min' : json.dumps(w_min, cls=NumpyEncoder),
        'w_max' : json.dumps(w_max, cls=NumpyEncoder),
    }
    return res

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5001)