# DS-X-Research-Moneyball

## Project Structure (The Directory Tree)

The core application is located in the demo/ directory. All data required to run the dashboard is stored in the data/ directory.

```
BU Topics Analysis/
├── data/
│   ├── bu_gap_score.csv         # Raw Gap Score data (used in some EDA)
├── demo/
│   ├── assets/
│   │   └── new_logo.png         # Application logo
│   ├── pages/
│   │   ├── 1_CountByTopic.py    # Time-series trend 
│   │   ├── 2_CountByCountry.py  # Geographic/Country 
│   │   ├── 3_GapScore.py        # Core Gap Score calculation
│   │   ├── 4_InterdisciplinaryScore.py
│   │   └── 5_SocialSentiment.py # Sentiment Analysis on social media
│   └── app.py                   # Main entry point and Weight Assignment page
├── eda/                         # Exploratory Data Analysis notebooks/scripts
│   ├── eda2.py                  # Exploratory code using OpenAlex API
│   └── eda3.py                  # Exploratory code using the .csv files downloaded from OpenAlex
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
