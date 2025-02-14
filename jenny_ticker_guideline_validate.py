import streamlit as st
import requests
import pandas as pd
import os

# Load API Key securely
api_key = st.secrets["fmp_api"]

def fetch_financial_data(ticker, financialattribute, period="Annual"):
    """Fetch financial data from the API."""
    url = f'https://financialmodelingprep.com/api/v3/{financialattribute}/{ticker}?period={period}&apikey={api_key}'
    response = requests.get(url)
    return response.json()

def calculate_growth(df, column, years):
    """Calculate the compound annual growth rate (CAGR)."""
    try:
        val1 = df.loc[0, [column]].iloc[0]  # Most recent year
        val2 = df.loc[years, [column]].iloc[0]  # N years ago
        growth_rate = (((val1 / val2) ** (1 / years)) - 1) * 100
        return f"{growth_rate:.2f}%"
    except Exception as e:
        return f"Error: {e}"

def analyze_ticker(ticker):
    """Perform 3-year and 5-year financial analysis on the given ticker."""
    
    # Income Statement Analysis
    income_data = fetch_financial_data(ticker, "income-statement")
    df_income = pd.DataFrame(income_data)

    rev_growth_3y = calculate_growth(df_income, "revenue", 2)
    rev_growth_5y = calculate_growth(df_income, "revenue", 4)
    
    net_income_growth_3y = calculate_growth(df_income, "netIncome", 2)
    net_income_growth_5y = calculate_growth(df_income, "netIncome", 4)

    # Cash Flow Analysis
    cash_flow_data = fetch_financial_data(ticker, "cash-flow-statement")
    df_cash_flow = pd.DataFrame(cash_flow_data)

    fcf_growth_3y = calculate_growth(df_cash_flow, "freeCashFlow", 2)
    fcf_growth_5y = calculate_growth(df_cash_flow, "freeCashFlow", 4)

    # Display Results
    st.subheader(f"Financial Analysis for {ticker.upper()}")
    st.write(f"**3-Year Revenue Growth Rate:** {rev_growth_3y}")
    st.write(f"**5-Year Revenue Growth Rate:** {rev_growth_5y}")
    st.write(f"**3-Year Net Income Growth Rate:** {net_income_growth_3y}")
    st.write(f"**5-Year Net Income Growth Rate:** {net_income_growth_5y}")
    st.write(f"**3-Year Free Cash Flow Growth Rate:** {fcf_growth_3y}")
    st.write(f"**5-Year Free Cash Flow Growth Rate:** {fcf_growth_5y}")

# Streamlit UI
st.title("Stock Growth Analyzer")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "").upper()

if ticker:
    analyze_ticker(ticker)
