import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_ticker_data(ticker):
    """
    Fetches the current spot price for a given ticker using Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol
        
    Returns:
        float or None: The current stock price or None if unavailable
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Récupérer les 5 derniers jours au lieu de 1
        data = stock.history(period="5d")  # Augmenter la période

        if data.empty:
            print(f"Aucune donnée trouvée pour {ticker}")
            return None
            
        # Prendre la dernière valeur de clôture disponible
        latest_price = data['Close'].dropna().iloc[-1]  # Éviter NaN
        
        return round(float(latest_price), 2)
        
    except Exception as e:
        print(f"Erreur détaillée lors de la récupération des données pour {ticker}: {str(e)}")
        return None
