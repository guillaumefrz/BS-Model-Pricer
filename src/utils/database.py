import sqlite3
import pandas as pd
from datetime import datetime

def initialize_database():
    """Initialise la base de données avec gestion des erreurs"""
    try:
        conn = sqlite3.connect("calculations.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                spot_price REAL NOT NULL,
                strike_price REAL NOT NULL,
                maturity REAL NOT NULL,
                risk_free_rate REAL NOT NULL,
                volatility REAL NOT NULL,
                call_purchase_price REAL NOT NULL,
                put_purchase_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT positive_check CHECK (
                    spot_price > 0 AND 
                    strike_price > 0 AND 
                    maturity > 0 AND 
                    volatility > 0
                )
            )
        """)
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {str(e)}")
        return False
    finally:
        conn.close()

def save_calculation(ticker, spot_price, strike_price, maturity, risk_free_rate, volatility, call_purchase_price, put_purchase_price):
    conn = sqlite3.connect("calculations.db")
    conn.execute("""
        INSERT INTO calculations (
            ticker, spot_price, strike_price, maturity, risk_free_rate, volatility, call_purchase_price, put_purchase_price
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticker, spot_price, strike_price, maturity, risk_free_rate, volatility, call_purchase_price, put_purchase_price))
    conn.commit()
    conn.close()

def get_all_calculations():
    conn = sqlite3.connect("calculations.db")
    df = pd.read_sql("SELECT * FROM calculations", conn)
    conn.close()
    return df
