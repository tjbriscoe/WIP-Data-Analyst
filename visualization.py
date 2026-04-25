#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 14:58:29 2025

@author: timothysmith
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
pio.renderers.default = "browser"
plt.style.use("ggplot")
from analysis import annual
from dash import Dash, html, dcc

def prepare_data(annual):
    
    annual = annual.copy()
    annual["Year"] = annual.index.year
    
    return annual


annual = prepare_data(annual)
    

def visualization(annual):
    
    annual = annual.copy()
    
    #Normalized Income Data
    annual["Normalized_Income"] = annual["median_income"] / annual["median_income"].iloc[0]
    annual["Normalized_CPI"] = annual["cpi"]/ annual["cpi"].iloc[0]
    
    fig, ax = plt.subplots(2,1, figsize =(12,8), sharex = True)
    
    ax[0].plot(
        annual["Year"], 
        annual["Normalized_Income"], 
        label ="Median Income(Indexed)")
    
    ax[0].plot(
        annual["Year"],
        annual["Adjusted Income"]/annual["Adjusted Income"].iloc[0], 
        label="Adjusted Income")
    
    ax[0].legend()  
    ax[0].set_ylabel("Income Index")
    ax[0].set_title("Income Trends")
    
    ax2 = ax[1].twinx()

    ax[1].plot(
        annual["Year"],
        annual["Normalized_CPI"],
        color="red", label="CPI(Indexed)"
        
        )
    ax[1].set_ylabel("Inflation(CPI)")
    ax2.legend(loc = "upper right")
    
    plt.xlabel("Year")
    plt.tight_layout()
    plt.show()
    
    
def visualization_interactive(df):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["median_income"],
        name="Median Income",
        mode="lines"
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Adjusted Income"],
        name="Adjusted Income",
        mode="lines"
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["cpi"],
        name="CPI",
        mode="lines",
        yaxis="y2",
        line=dict(color="green")
    ))

    fig.update_layout(
        title="Income vs Inflation (CPI)",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Income (USD)"),
        yaxis2=dict(
            title="CPI",
            overlaying="y",
            side="right"
        ),
        template="plotly_white",
        hovermode="x unified"
    )

    if 2008 in df["Year"].values:
        crisis_row = df[df["Year"] == 2008]
        fig.add_annotation(
            x=2008,
            y=crisis_row["Adjusted Income"].iloc[0],
            text="2008 Financial Crisis",
            showarrow=True,
            arrowhead=2
        )

    fig.show()

    return fig

