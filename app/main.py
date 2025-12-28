
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

