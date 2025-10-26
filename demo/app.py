# app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import os

LOGO_PATH = "demo/assets/new_logo.png" 
LOGO_WIDTH = 200 

# Check if the file exists (Good practice from previous step)
if not os.path.exists(LOGO_PATH):
    st.error(f"Logo file not found at: {LOGO_PATH}. Please check the file path.")
else:
    # 1. Create three columns to push the content to the center.
    # The ratio [1, 0.5, 1] means the center column is smaller than the sides, 
    # but we'll use a fixed width for the image to control the size precisely.
    col1, col2, col3 = st.columns([1, 0.5, 1])
    
    # 2. Place the image in the center column (col2)
    with col2:
        # Use the 'width' parameter to set a fixed, small size (e.g., 100px)
        st.image(LOGO_PATH, width=LOGO_WIDTH)

st.set_page_config(page_title="BU Research Navigator", layout="wide")

# Header with BU branding
st.markdown("""
    <h1 style='text-align: center; color: #CC0000;'>Welcome back!</h1>
    <h3 style='text-align: center; color: #666;'>Let's discover your next research opportunity.</h3>
    <hr style='margin-bottom: 30px;'>
""", unsafe_allow_html=True)


column_names = ['Field', 'CAGR', 'Gap Score', 'Social Velocity', 'Interdisciplinarity']

data = {
    column_names[0]: [
    'Artificial Intelligence in Healthcare', 
    'AI in Service Interactions', 
    'Advanced Mathematical Modeling in Engineering',
    'Privacy-Preserving Technologies in Data', 
    'CAR-T cell therapy research', 
    'FinTech, Crowdfunding, Digital Finance',
    'Robotic Path Planning Algorithms', 
    'Extraction and Separation Processes', 
    'Electric Vehicles and Infrastructure',
    'Nanoplatforms for cancer theranostics', 
    'Environmental Sustainability in Business', 
    'BIM and Construction Integration',
    'Stock Market Forecasting Methods', 
    'Black Holes and Theoretical Physics', 
    'Spectroscopy and Chemometric Analyses'
    ],

    # Column 1: CAGR
    column_names[1]: [
        0.2048, 0.0481, 0.0089, -0.0526, -0.0470, 
        0.0496, -0.0849, 0.0776, -0.0627, -0.0563, 
        -0.0145, 0.0045, -0.0258, -0.1758, -0.0490
    ],
    
    # Column 2: Gap Score
    column_names[2]: [
        0.9986, 0.9991, 0.9999, 0.9989, 0.9989,
        0.9996, 0.9993, 1, 0.9998, 0.9995,
        1, 0.9999, 0.9987, 0.9992, 0.9998

    ],
    
    # Column 3: Velocity Score
    column_names[3]: [
        3.125055, -0.474896, -0.823839, -0.730084, -0.700281,
        0.215539, 0, 0.397462, 0.83333, -0.193631, 
        0.10502, 0.208089, 0.509045, -0.752436, -0.700281
    ],
    
    # Column 4: Status (Boolean or Categorical)
    column_names[4]: [
        0.5316, 0.8049, 0.3051, 0.3254, 0.7903, 
        0.3209, 0.0195, 0.0228, 0.0741, 0.6437, 
        0.3542, 0.3778, 0.5643, 0.0044, 0.5831
    ]
}

metrics = pd.DataFrame(data)

# Weight Selection Section
st.markdown("### Customize Your Research Priorities")
st.markdown("Adjust the weights below based on what matters most to you:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    w_momentum = st.slider("**Pulibcation Momentum**", 0.0, 1.0, 0.25, 0.05,
                           help="How fast is this field growing?")    
    
with col2:
    w_gap = st.slider("**BU Gap Score**", 0.0, 1.0, 0.25, 0.05, 
                      help="How underrepresented is BU in this field?")
    
with col3:
    w_velocity = st.slider("**Social Velocity**", 0.0, 1.0, 0.25, 0.05,
                           help="How trending is this topic?")
    
with col4:
    w_interdisciplinary = st.slider("**Interdisciplinary Spread**", 0.0, 1.0, 0.25, 0.05,
                                    help="How cross-disciplinary is this field?")
    
# Check if weights sum to 1
weight_sum = w_gap + w_velocity + w_interdisciplinary + w_momentum

if abs(weight_sum - 1.0) > 0.01:
    st.warning(f"Weights currently sum to {weight_sum:.2f}. Please adjust to equal 1.0")
    # Auto-normalize
    w_gap_norm = w_gap / weight_sum if weight_sum > 0 else 0.25
    w_velocity_norm = w_velocity / weight_sum if weight_sum > 0 else 0.25
    w_interdisciplinary_norm = w_interdisciplinary / weight_sum if weight_sum > 0 else 0.25
    w_momentum_norm = w_momentum / weight_sum if weight_sum > 0 else 0.25
    st.info(f"Auto-normalized to: Gap={w_gap_norm:.2f}, Velocity={w_velocity_norm:.2f}, Interdisciplinary={w_interdisciplinary_norm:.2f}, Momentum={w_momentum_norm:.2f}")
else:
    st.success(f"Perfect! Weights sum to {weight_sum:.2f}")
    w_gap_norm = w_gap
    w_velocity_norm = w_velocity
    w_interdisciplinary_norm = w_interdisciplinary
    w_momentum_norm = w_momentum

# Calculate Composite Opportunity Score
metrics['Opportunity_Score'] = (
    w_gap_norm * metrics['Gap Score'] + 
    w_velocity_norm * metrics['Social Velocity'] + 
    w_interdisciplinary_norm * metrics['Interdisciplinarity'] + 
    w_momentum_norm * metrics['CAGR']
)

# Rank topics
metrics_ranked = (
    metrics
    .sort_values(by='Opportunity_Score', ascending=False) 
    .assign(Rank=lambda x: np.arange(len(x)) + 1)  
).reset_index()
metrics_ranked['Rank'] = metrics_ranked.index + 1

# Display Results
st.markdown("---")
st.markdown("### Your Personalized Research Opportunities")

# Full ranked table
st.markdown("### Complete Rankings")

# Prepare display dataframe
display_metrics = metrics_ranked[['Rank', 'Field', 'Opportunity_Score', 'CAGR', 'Gap Score', 'Social Velocity', 'Interdisciplinarity']]
display_metrics.columns = ['Rank', 'Field', 'Opportunity Score', 'Pulibcation Momentum', 'Gap Score', 'Social Velocity', 'Interdisciplinary Spread']

# Round scores
for col in ['Opportunity Score', 'Pulibcation Momentum', 'Gap Score', 'Interdisciplinary Spread', 'Social Velocity']:
    display_metrics[col] = display_metrics[col].round(3)

# Display with styling
st.dataframe(
    display_metrics.style.background_gradient(subset=['Opportunity Score'], cmap='RdYlGn', vmin=display_metrics['Opportunity Score'].min(), vmax=display_metrics['Opportunity Score'].max()),
    use_container_width=True,
    height=600
)

# Download button
csv = display_metrics.to_csv(index=False)
st.download_button(
    label="Download Results (CSV)",
    data=csv,
    file_name="bu_research_opportunities.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #999; font-size: 12px;'>
    Data-driven insights for BU research strategy • Adjust weights above to explore different priorities
    </p>
""", unsafe_allow_html=True)
