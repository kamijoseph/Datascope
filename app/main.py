
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
    page_icon = "📊"
)

st.title(" DataScope+ | Interactive Data Analyzer & Cleaner |")
st.markdown("""
Welcome to **DataScope+**, an interactive tool to explore, clean, and visualize your datasets.
Upload your CSV, Excel, or Stata files and get automated insights with interactive charts and EDA.
""")

# upload
uploaded_file = st.file_uploader(
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
    
# data cleaning function
def clean_data(df, strategy="auto"):
    cleaned_df = df.copy()
    for column in cleaned_df.columns:
        if cleaned_df[column].isnull().sum() > 0:
            if pd.api.types.is_datetime64_any_dtype(cleaned_df[column]):
                cleaned_df[column].fillna(cleaned_df[column].mean() if strategy=="auto" else 0, inplace=True)
            elif pd.api.types.is_datetime64_any_dtype(cleaned_df[column]):
                cleaned_df[column].fillna(cleaned_df[column].median(), inplace=True)
            else:
                cleaned_df[column].fillna(cleaned_df[column].mode()[0], inplace=True)
    return cleaned_df

# helper functions
def get_table_download_link(data, filename="cleaned_data.csv"):
    csv = data.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Cleaned CSV</a>'

def get_image_download_link(buf, filename="chart.png"):
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">Download Chart Image</a>'

# main logic
if uploaded_file:
    data = load_data(uploaded_file)
    if data is not None:
        st.success("File uploaded succesfully !!!")
        st.subheader("Preview Dataset: Top 10")
        st.dataframe(data.head(10))
        st.subheader("Preview Dataset: Bottom 10")
        st.dataframe(data.tail(10))
        st.markdown("---")

        st.subheader("Dataset Summary & INsights")

        # shape and dtypes expander
        with st.expander("Shape & Column Types"):
            st.write("**Rows X Columns:**", data.shape)
            st.dataframe(data.dtypes.rename("Data Type"))
        
        # missing values and dplicates expander
        with st.expander("Missing & Duplicate Values"):
            missing = data.isnull().sum()
            duplicates = data.duplicated().sum()
            st.write(f"**Duplicates:**", duplicates)
            st.write("**Missing Values:**")
            st.dataframe(
                missing[missing > 0].sort_values(ascending=False)
            )
            