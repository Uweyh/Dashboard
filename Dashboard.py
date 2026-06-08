import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="My First Dashboard", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_png_as_page_bg('SM.png')

st.sidebar.header("⚙️ Dashboard Controls")
st.sidebar.date_input("Select a date")

upload_file = st.sidebar.file_uploader("Upload your own dataset (CSV):", type=['csv'])

df = pd.read_csv("social_media_sleep_stress_productivity_11000.csv")

st.title(" Welcome to my Dashboard")
st.markdown("This is my first time using Streamlit, enhanced with dynamic analytics.")
st.write("---")

with st.expander("👀 View Raw Data Table"):
    st.dataframe(df, use_container_width=True)

st.write("---")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Histogram Analysis")
    column = st.selectbox("Choose a column for Histogram", df.columns, key="hist_select")
    
    fig_hist = px.histogram(df, x=column, title=f"Distribution of {column}", 
                            color_discrete_sequence=['#636EFA'])
    fig_hist.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_hist, use_container_width=True)

with col_chart2:
    st.subheader("📉 Scatter Chart Relationship")
    x_column = st.selectbox("Choose x-axis column", df.columns, key="scatter_x")
    y_column = st.selectbox("Choose y-axis column", df.columns, key="scatter_y")
    
    color_col = None
    if 'sex' in df.columns:
        color_col = 'sex'
    elif 'day' in df.columns:
        color_col = 'day'
        
    fig_scatter = px.scatter(df, x=x_column, y=y_column, color=color_col,
                             title=f"{y_column} vs {x_column}",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)
