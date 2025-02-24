import streamlit as st
import pandas as pd
import numpy as np
from BlackScholes import BlackScholes

from src.models.BlackScholes import BlackScholes
from src.utils.plotting import (
    generate_pnl_matrix,
    plot_pnl_heatmap_subplot,
    plot_3d_surface_subplot,
    plot_greeks_barchart,
)
from src.utils.database import save_calculation, get_all_calculations, initialize_database
from src.utils.helpers import calculate_purchase_prices
from src.utils.data_fetch import fetch_ticker_data
# Initialize Database
initialize_database()

# Page Configuration
st.set_page_config(page_title="Black-Scholes Dashboard", layout="wide")

# Tabs for Navigation
tabs = st.tabs(["Calculator", "History"])

# Tab 1: Calculator
with tabs[0]:
    st.title("Black-Scholes Option Pricing Model")

    # Sidebar Inputs
    st.sidebar.header("Market Data")
    popular_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA", "BABA", "DIS"
    ]
    ticker = st.sidebar.selectbox("Select a Ticker", options=popular_tickers, index=0)

    # Fetch Market Data
    if st.sidebar.button("Fetch Market Data"):
        try:
            market_price = fetch_ticker_data(ticker)
            if market_price is None:
                st.sidebar.error(f"Impossible de récupérer le prix pour {ticker}")
                market_price = st.session_state.get("spot_price", 240.0)
            else:
                st.sidebar.success(f"Prix spot récupéré : {market_price:.2f}")
                st.session_state["spot_price"] = market_price
        except Exception as e:
            st.sidebar.error(f"Erreur lors de la récupération des données : {str(e)}")
            market_price = st.session_state.get("spot_price", 240.0)
    else:
        market_price = st.session_state.get("spot_price", 240.0)

    # Input Parameters
    st.sidebar.header("Option Parameters")
    spot_price = st.sidebar.number_input("Spot Price (S)", value=market_price, step=1.0)
    strike_price = st.sidebar.number_input(
        "Strike Price (K)", value=round(spot_price * 0.95, 2), step=1.0
    )
    maturity = st.sidebar.number_input(
        "Maturity (T, years)", min_value=0.01, value=1.0, step=0.1
    )
    risk_free_rate = st.sidebar.number_input(
        "Risk-Free Rate (r)", min_value=0.0, value=0.05, step=0.01
    )
    volatility = st.sidebar.number_input(
        "Volatility (σ)", min_value=0.01, value=0.2, step=0.01
    )

    # Auto-calculate purchase prices
    call_price, put_price = calculate_purchase_prices(
        spot_price, strike_price, maturity, risk_free_rate, volatility
    )
    call_purchase_price = st.sidebar.number_input(
        "Call Purchase Price",
        value=round(call_price * 1.02, 2),
        step=0.1,
        help="Auto-initialized to +2% of the theoretical Call price.",
    )
    put_purchase_price = st.sidebar.number_input(
        "Put Purchase Price",
        value=round(put_price * 1.02, 2),
        step=0.1,
        help="Auto-initialized to +2% of the theoretical Put price.",
    )

    # P&L Ranges
    st.sidebar.header("Ranges for P&L")
    spot_min = st.sidebar.number_input("Min Spot", value=spot_price * 0.8, step=1.0)
    spot_max = st.sidebar.number_input("Max Spot", value=spot_price * 1.2, step=1.0)
    vol_min = st.sidebar.number_input("Min Volatility", value=volatility * 0.8, step=0.01)
    vol_max = st.sidebar.number_input("Max Volatility", value=volatility * 1.2, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 20)
    vol_range = np.linspace(vol_min, vol_max, 20)

    # Calculate Results
    if st.sidebar.button("Calculate"):
        try:
            st.header("Results")
            
            # Vérification des paramètres
            if spot_price <= 0 or strike_price <= 0 or maturity <= 0:
                st.error("Les prix et la maturité doivent être positifs")
                st.stop()
            
            if volatility <= 0 or volatility > 1:
                st.error("La volatilité doit être comprise entre 0 et 1")
                st.stop()

            # Generate P&L matrices
            pnl_call = generate_pnl_matrix(
                maturity, strike_price, risk_free_rate, call_purchase_price, spot_range, vol_range, option_type="call"
            )
            pnl_put = generate_pnl_matrix(
                maturity, strike_price, risk_free_rate, put_purchase_price, spot_range, vol_range, option_type="put"
            )

            # Black-Scholes model for Greeks
            bs_model = BlackScholes(maturity, strike_price, spot_price, volatility, risk_free_rate)
            greeks = bs_model.calculate_prices_and_greeks()

            # Save Calculation
            save_calculation(
                ticker, spot_price, strike_price, maturity, risk_free_rate, volatility, call_purchase_price, put_purchase_price
            )

            # Display Option Prices
            st.subheader("Option Prices")
            st.markdown(f"**Call Price (Black-Scholes)**: ${call_price:.2f}")
            st.markdown(f"**Put Price (Black-Scholes)**: ${put_price:.2f}")

            # P&L Heatmaps
            st.header("P&L Heatmaps")
            heatmap_fig = plot_pnl_heatmap_subplot(pnl_call, pnl_put, spot_range, vol_range)
            st.pyplot(heatmap_fig)

            # 3D Surfaces
            st.header("P&L 3D Surfaces")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Call P&L 3D Surface")
                call_surface_fig = plot_3d_surface_subplot(pnl_call, spot_range, vol_range, "Call P&L")
                st.plotly_chart(call_surface_fig)
            with col2:
                st.subheader("Put P&L 3D Surface")
                put_surface_fig = plot_3d_surface_subplot(pnl_put, spot_range, vol_range, "Put P&L")
                st.plotly_chart(put_surface_fig)

            # Greeks Visualization
            st.header("Greeks Visualization")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Call Greeks")
                call_greek_chart = plot_greeks_barchart(greeks, "call")
                st.plotly_chart(call_greek_chart)
            with col2:
                st.subheader("Put Greeks")
                put_greek_chart = plot_greeks_barchart(greeks, "put")
                st.plotly_chart(put_greek_chart)

        except Exception as e:
            st.error(f"Une erreur s'est produite lors des calculs : {str(e)}")

# Tab 2: History
with tabs[1]:
    st.title("Calculation History")
    history = get_all_calculations()
    if not history.empty:
        st.dataframe(history)
        st.download_button("Download History", data=history.to_csv(index=False), file_name="history.csv", mime="text/csv")
    else:
        st.info("No calculations saved yet.")
