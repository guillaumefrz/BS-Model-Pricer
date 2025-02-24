from src.models.BlackScholes import BlackScholes

def calculate_purchase_prices(spot_price, strike_price, maturity, risk_free_rate, volatility):
    """
    Calculate theoretical call and put prices using the Black-Scholes model.
    """
    bs_model = BlackScholes(maturity, strike_price, spot_price, volatility, risk_free_rate)
    call_price, put_price = bs_model.calculate_prices()
    return call_price, put_price
