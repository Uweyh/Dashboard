import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64

st.set_page_config(
    page_title="Dynamic Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1920&auto=format&fit=crop"

local_png_path = "SM.png" 
bg_image_base64 = get_base64_image(local_png_path)

st.markdown(
    f"""
    <style>
    /* 1. Main App Background */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)), url("{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* 2. Glassmorphism for standard layout cards (Metrics, Tabs, and Uploaders) */
    div[data-testid="stMetricBlock"], .stTabs, .stUploadDropzone {{
        background-color: rgba(255, 255, 255, 0.07) !important;
        padding: 20px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* 3. Safe Dataframe Styling (Prevents text blurring inside the table) */
    div[data-testid="stDataFrame"] {{
        background-color: rgba(20, 20, 20, 0.6) !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: none !important; /* Disables the blur that bleeds into text grid */
    }}
    
    /* 4. Global text element coloring */
    h1, h2, h3, p, label {{
        color: 
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Header Section & CSV File Uploader Widget
st.title("📈 Dynamic CSV Performance Dashboard")

df = pd.read_csv("social_media_sleep_stress_productivity_11000.csv")
# 5. Tab Layout Setup
tab1, tab2, tab3 = st.tabs(["📊 Visualizations", "🔍 Data Analysis", "⚙️ Raw Data Explorer"])

# Dynamic mapping helper based on what columns exist in user's CSV
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=[object, "category"]).columns.tolist()

with tab1:
    st.subheader("Dynamic Charting")
    
    if len(numeric_cols) >= 1:
        # Dynamic Chart Configuration selectors
        col_select1, col_select2 = st.columns(2)
        with col_select1:
            x_axis = st.selectbox("Select X-Axis metric:", options=df.columns.tolist(), index=0)
        with col_select2:
            y_axis = st.selectbox("Select Y-Axis metric:", options=numeric_cols, index=0)
            
        chart_col1, chart_col2 = st.columns([2, 1])
        
        with chart_col1:
            fig_trend = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}", template="plotly_dark")
            fig_trend.update_traces(line_color="#00cc96")
            fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with chart_col2:
            if len(categorical_cols) >= 1:
                cat_target = categorical_cols[0]
                df_cat = df.groupby(cat_target)[y_axis].sum().reset_index()
                fig_pie = px.pie(df_cat, values=y_axis, names=cat_target, title=f"Total {y_axis} by {cat_target}", template="plotly_dark", hole=0.4)
                fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.write("No text categories found in dataset to build a pie breakdown chart.")
    else:
        st.warning("Please upload a CSV dataset containing numeric metrics to render performance graphs.")

with tab2:
    st.subheader("Statistical Dataset Profile")
    
    if len(numeric_cols) > 0:
        st.markdown("**Descriptive Metrics Summary:**")
        st.dataframe(df.describe().round(2), use_container_width=True)
        
        if len(numeric_cols) >= 2:
            st.markdown("### Interactive Scatter Correlation")
            scat_x = st.selectbox("Scatter X Metric:", numeric_cols, index=0)
            scat_y = st.selectbox("Scatter Y Metric:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            
            fig_scatter = px.scatter(df, x=scat_x, y=scat_y, template="plotly_dark")
            fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.write("Provide numeric properties within your CSV data matrix to view automated statistical trends.")

with tab3:
    st.subheader("Interactive Dataset Viewer")
    st.info(f"Showing dataset workspace snapshot ({len(df)} total records).")
    st.dataframe(df, use_container_width=True)
