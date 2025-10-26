# DS-X-Research-Moneyball

##Project Structure (The Directory Tree)

The core application is located in the demo/ directory. All data required to run the dashboard is stored in the data/ directory.

```
BU Topics Analysis/
├── data/
│   ├── bu_gap_score.csv         # Raw Gap Score data (used in some EDA)
│   ├── t15_topic_summary.csv    # Trend data for visualization
│   └── concept_by_year.csv      # Time-series data breakdown (Example)
├── demo/
│   ├── assets/
│   │   └── new_logo.png         # Application logo
│   ├── pages/
│   │   ├── 1_CountByTopic.py    # Time-series trend page
│   │   ├── 2_CountByCountry.py  # Geographic/Country visualization
│   │   ├── 3_GapScore.py        # Core Gap Score calculation and display
│   │   ├── 4_InterdisciplinaryScore.py
│   │   └── 5_SocialSentiment.py
│   └── app.py                   # Main entry point and Weight Assignment page
├── eda/                         # Exploratory Data Analysis notebooks/scripts
│   ├── BU vs Global.ipynb       # Initial comparison of BU publications (Example)
│   └── eda2.py                  # Script for data cleaning (Example)
├── requirements.txt             # Required Python packages (pandas, streamlit, etc.)
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
