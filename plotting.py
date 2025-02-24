import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from BlackScholes import BlackScholes
import numpy as np

def generate_pnl_matrix(maturity, strike_price, risk_free_rate, purchase_price, spot_range, vol_range, option_type):
    """
    Generate a P&L matrix for either Call or Put options.
    """
    pnl_matrix = []
    for vol in vol_range:
        row = []
        for spot in spot_range:
            bs_model = BlackScholes(maturity, strike_price, spot, vol, risk_free_rate)
            if option_type == "call":
                theoretical_price, _ = bs_model.calculate_prices()
            else:  # "put"
                _, theoretical_price = bs_model.calculate_prices()
            pnl = theoretical_price - purchase_price
            row.append(pnl)
        pnl_matrix.append(row)
    return pnl_matrix

def plot_pnl_heatmap_subplot(pnl_call, pnl_put, spot_range, vol_range):
    """
    Create a heatmap subplot for Call and Put P&L matrices.
    """
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    sns.heatmap(pnl_call, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), ax=axs[0], cmap="RdYlGn", cbar=True)
    axs[0].set_title("Call P&L Heatmap")
    axs[0].set_xlabel("Spot Price")
    axs[0].set_ylabel("Volatility")

    sns.heatmap(pnl_put, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), ax=axs[1], cmap="RdYlGn", cbar=True)
    axs[1].set_title("Put P&L Heatmap")
    axs[1].set_xlabel("Spot Price")
    axs[1].set_ylabel("Volatility")

    plt.tight_layout()
    return fig

def plot_3d_surface_subplot(matrix, spot_range, vol_range, title):
    """
    Plot a 3D surface for Call or Put P&L matrix.
    """
    fig = go.Figure(
        data=[
            go.Surface(
                z=matrix,
                x=spot_range,
                y=vol_range,
                colorscale="Viridis",
                name=title,
            )
        ]
    )
    fig.update_layout(scene=dict(
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        zaxis_title="P&L",
    ))
    return fig

def plot_greeks_barchart(greeks, option_type):
    """
    Create a bar chart for Greeks.
    """
    greek_labels = [k for k in greeks.keys() if option_type in k]
    greek_values = [v for k, v in greeks.items() if option_type in k]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=greek_labels, y=greek_values, name=f"{option_type.capitalize()} Greeks"))

    fig.update_layout(
        title=f"{option_type.capitalize()} Greeks Visualization",
        xaxis_title="Greeks",
        yaxis_title="Value",
        barmode="group",
    )
    return fig
