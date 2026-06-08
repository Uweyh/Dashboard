import pandas as pd
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display, HTML, Audio
from datetime import datetime

# Load CSV
df = pd.read_csv("social_media_sleep_stress_productivity_11000.csv")

# Dashboard Title
display(HTML(f"""
<h1>Social Media, Sleep, Stress & Productivity Dashboard</h1>
<h3>{datetime.now().strftime("%d %B %Y %H:%M")}</h3>
"""))

# KPI
print("Total Records:", len(df))
print("Average Productivity Score:", round(df["ProductivityScore"].mean(), 2))
print("Average Sleep Hours:", round(df["SleepHours"].mean(), 2))
print("Average Social Media Hours:", round(df["SocialMediaHours"].mean(), 2))

# Interactive Graph
numeric_cols = df.select_dtypes(include="number").columns.tolist()

x_dropdown = widgets.Dropdown(
    options=numeric_cols,
    value="SleepHours",
    description="X Axis"
)

y_dropdown = widgets.Dropdown(
    options=numeric_cols,
    value="ProductivityScore",
    description="Y Axis"
)

def update_graph(x_col, y_col):
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color="StressLevel",
        hover_data=["Platform"],
        title=f"{y_col} vs {x_col}"
    )
    fig.show()

display(widgets.interactive(
    update_graph,
    x_col=x_dropdown,
    y_col=y_dropdown
))

# Heatmap
corr = df.select_dtypes(include="number").corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)
fig.show()

# Optional Music
# Audio("your_song.mp3", autoplay=False)



