# CountByCountry.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os

DATA_DIR = '../../data'
filename = 't15_topic_country_summary.csv'
file_path = os.path.join(DATA_DIR, filename)

# Read your summary table so topic names are index, columns are years
summary_table = pd.read_csv(file_path)
summary_table.columns = ['Topic', 'Country', 'Count', 'Year']
summary_table['Year'] = summary_table['Year'].astype(str)

st.title("Topic and Country Trends Dashboard ")
st.markdown("Use the controls in the sidebar to filter the data and update the chart.")

st.sidebar.header("Filter Options")

# 1. Topic Multiselect (Equivalent to your original 'select_topics')
all_topics = summary_table['Topic'].unique().tolist()
select_topics = st.sidebar.multiselect(
    "Choose **Topics** to plot:", 
    all_topics, 
    default=all_topics[:2]
)

# 2. Country Multiselect (The new filter you requested)
all_countries = summary_table['Country'].unique().tolist()
select_countries = st.sidebar.multiselect(
    "Choose **Countries**:", 
    all_countries, 
    default=all_countries
)

# 3. Year Range Slider (Equivalent to your original 'min_year, max_year')
years = sorted(summary_table['Year'].unique().tolist())
if years:
    min_year, max_year = st.sidebar.select_slider(
        "Select **Year Range**", 
        options=years, 
        value=(years[0], years[-1])
    )
    year_cols = [year for year in years if min_year <= year <= max_year]
else:
    year_cols = []


# --- DATA FILTERING ---
summary_table_filtered = summary_table[
    summary_table['Topic'].isin(select_topics) &
    summary_table['Country'].isin(select_countries) &
    summary_table['Year'].isin(year_cols)
]

summary_table_grouped = summary_table_filtered.groupby(['Year', 'Topic', 'Country'])['Count'].sum().reset_index()
summary_table_grouped['Topic_Country'] = summary_table_grouped['Topic'] + " - " + summary_table_grouped['Country']



if summary_table_grouped.empty:
    st.warning("No data available based on current filter selections.")
else:
    fig = px.line(
        summary_table_grouped,
        x='Year',
        y='Count',
        color='Topic_Country', # Plot a separate line for each Topic-Country combo
        markers=True,
        title="Count Trends by Topic and Country Over Time"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Count",
        legend_title="Topic - Country",
        hovermode="x unified" # Great for interactive comparison
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Display the aggregated table
    st.subheader("Aggregated Data Preview")
    summary_table_grouped = summary_table_grouped.iloc[:, :-1]  # Remove the combined column for cleaner display
    st.dataframe(summary_table_grouped)
