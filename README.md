# BS-Model-Pricer
# Black-Scholes Option Analytics Dashboard

## Overview
An interactive web application for option pricing and analysis using the Black-Scholes model. This tool provides real-time calculations, interactive visualizations, and comprehensive Greeks analysis.

## Features
- **Real-time Market Data**: Fetch live stock prices from Yahoo Finance
- **Option Pricing**: Calculate call and put option prices using Black-Scholes model
- **Greeks Analysis**: Compute and visualize Delta, Gamma, Vega, Theta, and Rho
- **Interactive Visualizations**:
  - P&L Heatmaps for sensitivity analysis
  - 3D Surface plots for price/volatility relationships
  - Greeks visualization charts
- **Data Persistence**: Save calculations and analysis in SQLite database

## Tech Stack
- **Frontend**: Streamlit
- **Data Processing**: yfinance, pandas, numpy
- **Visualization**: plotly, seaborn, matplotlib
- **Database**: SQLite
- **Mathematical Models**: scipy

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/black-scholes-dashboard.git

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Usage
1. Select a stock ticker from the dropdown menu
2. Fetch real-time market data
3. Adjust option parameters (Strike, Maturity, Volatility, etc.)
4. View calculated prices and Greeks
5. Analyze P&L through interactive visualizations

## Target Users
- Financial Analysts
- Options Traders
- Finance Students
- Risk Managers

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
