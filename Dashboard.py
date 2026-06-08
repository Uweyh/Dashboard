import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman (Buat layout jadi lebar/wide)
st.set_page_config(page_title="My First Dashboard", layout="wide")

# Paparkan gambar header
st.image('SM.png', use_container_width=True)
# 2. SIDEBAR - Tempat letak kawalan (Controls)
st.sidebar.header("⚙️ Dashboard Controls")
st.sidebar.date_input("Select a date")

# Fungsi upload fail yang berfungsi sepenuhnya
upload_file = st.sidebar.file_uploader("Upload your own dataset (CSV):", type=['csv'])

# Logik untuk membaca data (Guna data upload ATAU data default Tips.csv)
df = pd.read_csv("social_media_sleep_stress_productivity_11000.csv")

# 3. UTAMA - Tajuk Dashboard
st.title(" Welcome to my Dashboard")
st.markdown("This is my first time using Streamlit, enhanced with dynamic analytics.")
st.write("---")

# 4. TAMBAHAN BONUS: KPI Metrics Section
st.subheader("📊 Data Highlights (KPIs)")
if 'total_bill' in df.columns and 'tip' in df.columns:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="💰 Total Bill ($)", value=f"{df['total_bill'].sum():,.2f}")
    with col2:
        st.metric(label="💸 Total Tips ($)", value=f"{df['tip'].sum():,.2f}")
    with col3:
        st.metric(label="📈 Avg Bill ($)", value=f"{df['total_bill'].mean():,.2f}")
    with col4:
        st.metric(label="👥 Total Records", value=len(df))
else:
    st.info("KPIs akan dipaparkan jika ruangan 'total_bill' dan 'tip' wujud.")

st.write("---")

# 5. Papar Data (Guna Expander supaya tak semak)
with st.expander("👀 View Raw Data Table"):
    st.dataframe(df, use_container_width=True)

st.write("---")

# 6. Susun Carta Sebelah-menyebelah (Columns Layout)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Histogram Analysis")
    # Ditambah 'key' supaya tidak crash dengan selectbox lain
    column = st.selectbox("Choose a column for Histogram", df.columns, key="hist_select")
    
    # Guna Plotly untuk impak visual yang lebih moden
    fig_hist = px.histogram(df, x=column, title=f"Distribution of {column}", 
                            color_discrete_sequence=['#636EFA'])
    fig_hist.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_hist, use_container_width=True)

with col_chart2:
    st.subheader("📉 Scatter Chart Relationship")
    # Ditambah 'key' untuk elakkan ralat Streamlit Duplicate Widget ID
    x_column = st.selectbox("Choose x-axis column", df.columns, key="scatter_x")
    y_column = st.selectbox("Choose y-axis column", df.columns, key="scatter_y")
    
    # Letak warna mengikut kategori sekiranya ada kolum 'sex' atau 'day'
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
