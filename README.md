# DS-X-Research-Moneyball

## Project Structure (The Directory Tree)

The core application is located in the demo/ directory. All data required to run the dashboard is stored in the data/ directory.

```
BU Topics Analysis/
├── data/
│   └── bu_gap_score.csv         # Raw Gap Score data (used for calculation)
├── Interdiciplinary_ratio_top15.ipynb # Analysis of interdisciplinary spread across research topics
├── BU vs Global.ipynb           # Notebook used to calculate the initial gap score metrics
├── demo/
│   ├── assets/
│   │   └── new_logo.png         # Application logo
│   ├── pages/
│   │   ├── 1_CountByTopic.py    # Time-series trend page (Momentum Score)
│   │   ├── 2_CountByCountry.py  # Geographic/Country visualization
│   │   ├── 3_GapScore.py        # Core Gap Score visualization and application
│   │   ├── 4_InterdisciplinaryScore.py # Interdisciplinary Spread visualization
│   │   └── 5_SocialSentiment.py # Sentiment Analysis on social media trends
│   └── app.py                   # Main entry point and Weight Assignment page
├── requirements.txt             # Required Python packages (pandas, streamlit, etc.)
├── eda/                         # Exploratory Data Analysis notebooks/scripts
│   ├── eda2.py                  # Exploratory code using OpenAlex API
│   └── eda3.py                  # Exploratory code using the .csv files downloaded from OpenAlex
└── README.md                    # This file.
```


## Getting Started

Prerequisites

```
You need Python 3.8+ installed.
```

Installation

Clone the repository:
```
git clone [Your-Repo-URL]
cd BU-Research-Moneyball
```


Install dependencies:
```
pip install -r requirements.txt
```


Run the Streamlit application from the demo directory:
```
streamlit run demo/app.py
```
