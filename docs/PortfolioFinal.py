# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.19.10",
#     "pandas>=2.3.3",
#     "plotly>=6.5.1",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

app = marimo.App()

@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import numpy as np
    return mo, pd, px, np


@app.cell
def _(pd):
    # 🌍 REAL DATA: CO2 + GDP dataset
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

    df = pd.read_csv(url)

    # Clean + focus only useful columns
    df = df[[
        "country",
        "year",
        "co2_per_capita",
        "gdp",
        "population"
    ]]

    df = df.dropna()
    df = df[df["year"] >= 2000]

    return df,


@app.cell
def _(df, mo):
    countries = sorted(df["country"].unique())

    country_selector = mo.ui.multiselect(
        options=countries,
        value=["United Kingdom", "United States", "Germany", "France"],
        label="Select Countries"
    )

    return country_selector,


@app.cell
def _(df, country_selector):
    df_filtered = df[df["country"].isin(country_selector.value)]

    avg_emissions = df_filtered["co2_per_capita"].mean()

    return df_filtered, avg_emissions


@app.cell
def _(df_filtered, px, np):

    fig = px.scatter(
        df_filtered,
        x="gdp",
        y="co2_per_capita",
        color="country",
        size="population",
        hover_name="country",
        title="GDP vs CO₂ Emissions Per Capita",
        template="presentation"
    )

    # Trend line
    if not df_filtered.empty:
        x = df_filtered["gdp"]
        y = df_filtered["co2_per_capita"]

        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = intercept + slope * x_line

        fig.add_scatter(x=x_line, y=y_line, mode="lines", name="Trend")

    return fig,


@app.cell
def _(mo, country_selector, fig, df_filtered, avg_emissions):

    return mo.md(f"""
# 🌍 CO₂ & GDP Analysis Dashboard

## Filters
{country_selector}

## Key Metric
- Average CO₂ per capita: **{avg_emissions:.2f}**

## Chart
{mo.ui.plotly(fig)}

## Insight
- Higher GDP countries tend to have different emission patterns
- This helps analyse economic development vs environmental impact
""")

if __name__ == "__main__":
    app.run()