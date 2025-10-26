# InterdisciplinarySpread.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import os

st.set_page_config(page_title="Interdisciplinary Spread", layout="wide")
st.title("Interdisciplinary Ratio within Research Topics")
         
script_dir = Path(__file__).resolve().parent

csv_path = script_dir.parent.parent / 'BU Topics Analysis' / 'data' / 'inter_ratio.csv'

pair_dist_image_path = script_dir.parent / 'assets' / 'pair_distribution.png'

st.subheader("Percentage Distribution of Co-occurrence Pairs within Research Field (Total 5 years)")

if os.path.exists(pair_dist_image_path):
    # Use st.image with use_column_width=True for a large, wide display
    st.image(
        str(pair_dist_image_path), 
        caption="Pairwise Distribution Across All Metrics", 
        use_container_width=True
    )
else:
    st.warning(f"Image not found at: {pair_dist_image_path}. Please verify the path in your 'assets/' folder.")

st.markdown("---")

st.subheader("Interdisciplinary Ratio Data")

if os.path.exists(csv_path):
    try:
        # Load the DataFrame
        # The first column (Topic Names) is the index_col=0
        df = pd.read_csv(csv_path, index_col=0) 
        
        #st.info(f"Data loaded successfully from: {csv_path.relative_to(Path(__file__).parent.parent.parent)}")
        
        # ------------------------------------------------------------------
        # Clean up column names and configure display formatting
        # ------------------------------------------------------------------
        df.columns = ['Total Count', 'Number of Pairs', 'Interdisciplinary Ratio (%)']
        st.dataframe(
            df.style.format({
                # Apply number formatting directly to the DataFrame style for percentages and counts
                'Total Count': '{:,.0f}'.format,
                'Number of Pairs': '{:,.0f}'.format,
                'Interdisciplinary Ratio (%)': '{:.2f}'.format
            }),
            use_container_width=True
        )

    except Exception as e:
        # Catch the exception, but remove the specific column_config error to reveal others
        st.error(f"Error loading or reading CSV file: {e}")

else:
    st.error(f"CSV file not found at expected path: {csv_path}")
    st.markdown("Please ensure `inter_ratio.csv` is located in the `data/` folder.")
