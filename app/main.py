
# dependencies
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io
import base64

# app configuration
st.set_page_config(
    page_title = "DataScope+",
    layout = "wide",
    page_icon = "📈"
)

st.title("📊 DataScope+ | Interactive Data Analyzer & Cleaner")
st.markdown("""
Welcome to **DataScope+**, an interactive tool to explore, clean, and visualize your datasets.
Upload your CSV, Excel, or Stata files and get automated insights with interactive charts and EDA.
""")

# upload
uploaded_life = st.file_uploader(
    "Upload Dataset (csv, xlsx, xls, dta)",
    type = ["csv", "xlsx", "xls", "dta"]
)

# load data
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            xls = pd.ExcelFile(file)
            sheet = st.selectbox("Select Excel sheet", xls.sheet_names)
            return pd.read_excel(xls, sheet_name=sheet, engine="openpyxl")
        elif file.name.endswith(".xls"):
            xls = pd.ExcelFile(file, engine="xlrd")
            sheet = st.selectbox("Select Excel sheet", xls.sheet_names)
            return pd.read_excel(xls, sheet_name=sheet, engine="xlrd")
        elif file.name.endswith(".dta"):
            return pd.read_stata(file)
        else:
            st.error("Unsupported file format!!!")
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None