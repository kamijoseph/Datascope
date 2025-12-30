
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
def clean_data(df, strategy):
    cleaned_df = df.copy()

    if strategy == "drop":
        return cleaned_df.dropna()

    for column in cleaned_df.columns:
        if cleaned_df[column].isnull().sum() > 0:
            if pd.api.types.is_datetime64_any_dtype(cleaned_df[column]):
                if strategy == "auto":
                    cleaned_df[column].fillna(cleaned_df[column].mean(), inplace=True)
                elif strategy == "zero":
                    cleaned_df[column].fillna(0, inplace=True)

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

        # summary and data insighst
        st.subheader("Dataset Summary & Insights")

        # shape and dtypes expander
        with st.expander("Shape & Column Types"):
            st.write("**Rows X Columns:**", data.shape)
            st.dataframe(data.dtypes.rename("Data Type"))
        
        # missing values and dplicates expander
        with st.expander("Missing Values & Duplicate Values"):
            missing = data.isnull().sum()
            duplicates = data.duplicated().sum()
            st.write(f"**Duplicates:**", duplicates)
            st.write("**Missing Values:**")
            st.dataframe(
                missing[missing > 0].sort_values(ascending=False)
            )
        
        # brief stats expander
        with st.expander("Brief Numerical Stats"):
            st.dataframe(
                data.describe().T
            )
        
        # outliiers expander
        with st.expander("Outliers (Numeric)"):
            numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
            for column in numeric_cols:
                Q1 = data[column].quantile(0.25)
                Q3 = data[column].quantile(0.75)
                IQR = Q3 - Q1
                outliers = data[
                    (data[column] < Q1 - 1.5 * IQR) | (data[column] > Q3 + 1.5 * IQR)
                ][column]
                outliers_count = len(outliers)
                st.write(
                    f"**{column}**: {outliers_count} outliers detected!"
                )
        
        st.sidebar.header("Data Cleaning Options")
        cleaning_strategy = st.sidebar.radio(
            "Fill Missing Values Strategy",
            ["auto", "zero", "drop"]
        )
        enable_cleaning = st.sidebar.checkbox(
            "Enbale Cleaning",
            True
        )

        if enable_cleaning:
            data_cleaned = clean_data(data, cleaning_strategy)

            st.subheader("Cleaned Dataset Preview: Top 10")
            st.dataframe(data_cleaned.head(10))

            st.subheader("Cleaned Dataset Preview: Bottom 10")
            st.dataframe(data_cleaned.tail(10))
        else:
            data_cleaned = data

        # download link
        st.markdown(
            get_table_download_link(data_cleaned),
            unsafe_allow_html = True
        )

        with st.expander("Cleaned data shape & missing values"):
            st.write("**Rows X Columns:**", data_cleaned.shape)
            st.write("**Missing values for cleaned data:**")
            missing_cleaned = data_cleaned.isnull().sum()
            st.dataframe(
                missing_cleaned[missing_cleaned > 0].sort_values(ascending=False)
            )
        st.markdown("---")

        # column select for eda and vizz
        st.subheader("Column Selection for EDA & Visualization")
        selected_columns = st.multiselect(
            "**Choose Columns to Visualize**",
            data_cleaned.columns.tolist(),
            default = data_cleaned.columns.tolist()
        )
        data_filtered = data_cleaned[selected_columns]

        # Visualizations
        st.subheader("Visualization")
        chart_tab = st.tabs([
            "**Seaborn Charts**",
            "**Plotly Interactive Charts**"
        ])

        # seaborn charts
        with chart_tab[0]:
            chart_type = st.selectbox(
                "Select Seaborn Plot Type",
                ["Line Plot", "Bar Plot", "Scatter Plot", "Box Plot", "Histogram", "Heatmap", "Pie Chart"]
            )
            buf = io.BytesIO()

            # pie charts
            if chart_type == "Pie Chart":
                pie_col = st.selectbox("**Column for Pie Chart**", selected_columns)
                st.write(f"**IF THE CHART LOOKS WEIRD, YOU SHOULDNT BE USING THE {chart_type.upper()} FOR THE SELECTED COLUMN**")
                counts = data_filtered[pie_col].value_counts()
                fig, ax = plt.subplots(figsize=(6,6))
                ax.pie(
                    counts,
                    labels = counts.index,
                    autopct = "%1.1f%%",
                    startangle = 90
                )
                ax.axis("equal")
                st.pyplot(fig)
                fig.savefig(buf, format="png")
            else:
                x_axis = st.selectbox("X-axis", selected_columns)
                y_axis = st.selectbox("Y-axis", selected_columns)
                fig, ax = plt.subplots(figsize=(10, 6))

                # line chart
                if chart_type == "Line Plot":
                    sns.lineplot(
                        data = data_filtered,
                        x = x_axis,
                        y = y_axis,
                        ax = ax
                    )
                
                # bar chart
                elif chart_type == "Bar Plot":
                    sns.barplot(
                        data = data_filtered,
                        x = x_axis,
                        y = y_axis,
                        ax = ax
                    )
                
                # scatter plot