# SocialSentiment.py

import streamlit as st
import pandas as pd
import requests
import time
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="BU Research Social Velocity", layout="wide")

st.title("BU Research Social Velocity Dashboard")

# ==========================
# --- Load or Fetch DOIs ---
# ==========================
@st.cache_data(ttl=3600)
def fetch_openalex_dois(topics, max_results=20):
    topic_data = []
    for t in tqdm(topics, desc="Fetching DOIs"):
        base = "https://api.openalex.org/works"
        params = {
            "filter": f"title.search:{t.split('/')[0].strip()}",
            "sort": "relevance_score:desc",
            "per-page": max_results
        }
        try:
            r = requests.get(base, params=params, timeout=30)
            if r.status_code != 200:
                dois = []
            else:
                data = r.json().get("results", [])
                dois = [item.get("doi", "").replace("https://doi.org/", "") for item in data if item.get("doi")]
        except Exception:
            dois = []

        topic_data.append({
            "topic": t,
            "num_dois": len(dois),
            "dois": dois
        })
        time.sleep(0.5)
    return pd.DataFrame(topic_data)

topics = [
    "Artificial Intelligence in Healthcare / Artificial Intelligence in Healthcare and Education / Explainable Artificial Intelligence (XAI)",
    "AI in Service Interactions / AI in cancer detection",
    "Advanced Mathematical Modeling in Engineering / Advanced Nanomaterials in Catalysis / Spectral Theory in Mathematical Physics / advanced mathematical theories",
    "Privacy-Preserving Technologies in Data",
    "CAR-T cell therapy research",
    "Robotic Path Planning Algorithms",
    "Extraction and Separation Processes",
    "Electric Vehicles and Infrastructure",
    "Nanoplatforms for cancer theranostics",
    "Environmental Sustainability in Business",
    "BIM and Construction Integration",
    "Stock Market Forecasting Methods",
    "Black Holes and Theoretical Physics / Cold Atom Physics and Bose-Einstein Condensates / Physics of Superconductivity and Magnetism",
    "Spectroscopy and Chemometric Analyses"
]

df_results = fetch_openalex_dois(topics)

# ==========================
# --- Crossref Social Velocity ---
# ==========================
@st.cache_data(ttl=3600)
def fetch_social_velocity(df):
    def get_crossref_events(doi):
        base = "https://api.eventdata.crossref.org/v1/events"
        params = {"obj-id": f"https://doi.org/{doi}", "rows": 1000}
        try:
            r = requests.get(base, params=params, timeout=20)
            if r.status_code != 200:
                return 0
            data = r.json().get("message", {}).get("events", [])
            return len(data)
        except Exception:
            return 0

    social_velocity = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Crossref social velocity"):
        dois = row["dois"]
        if not dois:
            social_velocity.append(0)
            continue
        total_events = 0
        for doi in dois:
            total_events += get_crossref_events(doi)
            time.sleep(0.2)
        social_velocity.append(total_events)
    df["total_social_velocity"] = social_velocity

    # z-score normalization
    mean_velocity = np.mean(df["total_social_velocity"])
    std_velocity = np.std(df["total_social_velocity"])
    df["social_velocity_zscore"] = (df["total_social_velocity"] - mean_velocity) / std_velocity
    return df

df_results = fetch_social_velocity(df_results)

# ==========================
# --- Short Names ---
# ==========================
short_names = {
    "Artificial Intelligence in Healthcare / Artificial Intelligence in Healthcare and Education / Explainable Artificial Intelligence (XAI)": "AI Healthcare",
    "AI in Service Interactions / AI in cancer detection": "AI Service/Cancer",
    "Advanced Mathematical Modeling in Engineering / Advanced Nanomaterials in Catalysis / Spectral Theory in Mathematical Physics / advanced mathematical theories": "Advanced Math/Physics",
    "Privacy-Preserving Technologies in Data": "Privacy Tech",
    "CAR-T cell therapy research": "CAR-T Therapy",
    "Robotic Path Planning Algorithms": "Robotics Path",
    "Extraction and Separation Processes": "Extraction/Separation",
    "Electric Vehicles and Infrastructure": "EV & Infra",
    "Nanoplatforms for cancer theranostics": "Cancer Nanoplatforms",
    "Environmental Sustainability in Business": "Sustainability",
    "BIM and Construction Integration": "BIM & Construction",
    "Stock Market Forecasting Methods": "Stock Forecasting",
    "Black Holes and Theoretical Physics / Cold Atom Physics and Bose-Einstein Condensates / Physics of Superconductivity and Magnetism": "Physics: Black Holes/Condensates",
    "Spectroscopy and Chemometric Analyses": "Spectroscopy/Chemometrics"
}
df_results["topic_short"] = df_results["topic"].map(short_names)

# ==========================
# --- Table ---
# ==========================
st.subheader("Topic Table")
st.dataframe(df_results[["topic_short", "num_dois", "total_social_velocity", "social_velocity_zscore"]])

# ==========================
# --- Multi-Line Plot ---
# ==========================
st.subheader("Output vs Social Velocity")
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(df_results["topic_short"], df_results["num_dois"]/df_results["num_dois"].max(), 
        label="Relative Number of DOIs", marker="o", linewidth=2, color="gray", alpha=0.7)
ax.plot(df_results["topic_short"], df_results["total_social_velocity"]/df_results["total_social_velocity"].max(), 
        label="Relative Social Velocity", marker="o", linewidth=2, color="deepskyblue")
ax.set_ylabel("Relative Scale (0–1)")
ax.set_xticklabels(df_results["topic_short"], rotation=45, ha="right")
ax.legend()
ax.grid(linestyle="--", alpha=0.6)
st.pyplot(fig)

# ==========================
# --- Bar Plot: Z-score ---
# ==========================
st.subheader("Social Velocity Z-Scores by Topic")
df_viz = df_results.sort_values("total_social_velocity", ascending=False)
fig2, ax2 = plt.subplots(figsize=(12,6))
sns.barplot(
    data=df_viz,
    x="social_velocity_zscore",
    y="topic_short",
    palette="coolwarm",
    ax=ax2
)
ax2.axvline(0, color='black', linestyle='--', lw=1)
ax2.set_xlabel("Z-score (Relative to All Topics)")
ax2.set_ylabel("Research Topic")
st.pyplot(fig2)
