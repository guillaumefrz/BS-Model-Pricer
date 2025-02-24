from numpy import exp, sqrt, log
from scipy.stats import norm


class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(self):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
            log(current_price / strike)
            + (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
        ) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)

        call_price = current_price * norm.cdf(d1) - (
            strike * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
        )
        put_price = (
            strike * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2)
            - current_price * norm.cdf(-d1)
        )

        self.call_price = call_price
        self.put_price = put_price

        return call_price, put_price

    def calculate_greeks(self):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
            log(current_price / strike)
            + (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
        ) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)

        # Delta
        self.call_delta = norm.cdf(d1)
        self.put_delta = self.call_delta - 1

        # Gamma
        self.call_gamma = norm.pdf(d1) / (
            current_price * volatility * sqrt(time_to_maturity)
        )
        self.put_gamma = self.call_gamma

        # Vega
        self.call_vega = current_price * norm.pdf(d1) * sqrt(time_to_maturity)
        self.put_vega = self.call_vega

        # Theta
        self.call_theta = (
            -(
                current_price * norm.pdf(d1) * volatility
            ) / (2 * sqrt(time_to_maturity))
            - interest_rate
            * strike
            * exp(-interest_rate * time_to_maturity)
            * norm.cdf(d2)
        )
        self.put_theta = (
            -(
                current_price * norm.pdf(d1) * volatility
            ) / (2 * sqrt(time_to_maturity))
            + interest_rate
            * strike
            * exp(-interest_rate * time_to_maturity)
            * norm.cdf(-d2)
        )

        # Rho
        self.call_rho = (
            strike
            * time_to_maturity
            * exp(-interest_rate * time_to_maturity)
            * norm.cdf(d2)
        )
        self.put_rho = (
            -strike
            * time_to_maturity
            * exp(-interest_rate * time_to_maturity)
            * norm.cdf(-d2)
        )

    def calculate_prices_and_greeks(self):
        self.calculate_prices()
        self.calculate_greeks()
        greeks = {
            "call_price": self.call_price,
            "put_price": self.put_price,
            "call_delta": self.call_delta,
            "put_delta": self.put_delta,
            "call_gamma": self.call_gamma,
            "put_gamma": self.put_gamma,
            "call_vega": self.call_vega,
            "put_vega": self.put_vega,
            "call_theta": self.call_theta,
            "put_theta": self.put_theta,
            "call_rho": self.call_rho,
            "put_rho": self.put_rho,
        }
        return greeks