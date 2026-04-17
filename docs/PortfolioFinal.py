# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pandas",
#     "plotly",
#     "numpy",
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
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

    df = pd.read_csv(url)

    df = df[["country", "year", "co2_per_capita", "gdp", "population"]]
    df = df.dropna()
    df = df[df["year"] >= 2000]

    return df


@app.cell
def _(df, mo):
    countries = sorted(df["country"].unique())

    selector = mo.ui.multiselect(
        options=countries,
        value=["United Kingdom", "United States"],
        label="Select Countries"
    )

    return selector


@app.cell
def _(df, selector):
    filtered = df[df["country"].isin(selector.value)]
    avg = filtered["co2_per_capita"].mean()

    return filtered, avg


@app.cell
def _(filtered, px, np):
    clean = filtered.dropna(subset=["gdp", "co2_per_capita"])

    fig = px.scatter(
        clean,
        x="gdp",
        y="co2_per_capita",
        color="country",
        size="population",
        title="GDP vs CO₂ per Capita (2000+)",
    )

    if len(clean) > 1:
        x = clean["gdp"]
        y = clean["co2_per_capita"]

        m, b = np.polyfit(x, y, 1)

        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = m * x_line + b

        fig.add_scatter(x=x_line, y=y_line, mode="lines", name="Trend")

    return fig


@app.cell
def _(mo, selector, fig, avg):
    return mo.md(f"""
# 🌍 Data Literacy Portfolio

## 👤 About Me
This portfolio demonstrates my ability to work with real-world datasets using Python, Pandas, and Plotly.

---

## 📊 Interactive Analysis
Select countries to explore CO₂ emissions vs GDP.

{selector}

---

## 📈 Visualization
{mo.ui.plotly(fig)}

---

## 🌱 Insight
Average CO₂ per capita (selected countries): **{avg:.2f}**

---

## 🛠 Skills Demonstrated
- Data cleaning (Pandas)
- Interactive UI (Marimo widgets)
- Data visualization (Plotly)
- Trend analysis (linear regression)
""")