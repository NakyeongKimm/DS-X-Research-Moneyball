# CountByTopic.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os

st.title("Trends by Topic (2021–2025)")

DATA_DIR = '../../data'
filename = 't15_topic_summary.csv'
file_path = os.path.join(DATA_DIR, filename)

# Read your summary table so topic names are index, columns are years
summary_table = pd.read_csv(file_path, index_col=0)

years = ['2021', '2022', '2023', '2024', '2025']
#summary_table = summary_table.iloc[:, :-1] 

# Let user pick topics
topics = list(summary_table.index)
select_topics = st.multiselect("Choose topics to plot:", topics, default=topics[:5])

# Let user choose year range
min_year, max_year = st.select_slider(
    "Select year range", options=years, value=(years[0], years[-1])
)
year_cols = [year for year in years if min_year <= year <= max_year]

# Prepare the figure
fig = go.Figure()
for topic in select_topics:
    fig.add_trace(go.Scatter(
        x=year_cols,
        y=summary_table.loc[topic, year_cols],
        mode='lines+markers',
        name=topic
    ))

fig.update_layout(
    title="Topic Trends",
    xaxis_title="Year",
    yaxis_title="Value",
    legend_title="Topic"
)

st.plotly_chart(fig, use_container_width=True)

cagr_decimal_values = [
    0.2048, 0.0481, 0.0089, -0.0526, -0.0470, 
    0.0496, -0.0849, 0.0776, -0.0627, -0.0563, 
    -0.0145, 0.0045, -0.0258, -0.1758, -0.0490
]

summary_table['CAGR'] = [f"{val}" for val in cagr_decimal_values]

st.subheader("Data Table with CAGR")
st.dataframe(summary_table, use_container_width=True)

