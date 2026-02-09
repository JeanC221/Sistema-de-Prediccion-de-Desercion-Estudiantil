# Student Dropout Prediction System 

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange.svg)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

##  Overview
This project is an advanced analytical tool designed to identify students at risk of academic desertion. Developed as a final project at Universidad del Norte, it leverages Machine Learning to process complex datasets and provide actionable insights for early educational intervention.

**Impact:** Awarded academic recognition for technical excellence and its potential to reduce dropout rates through data-driven strategies.

---

##  Key Features
* **Automated Data Pipeline:** Robust cleaning, normalization, and handling of missing values using **Pandas** and **NumPy**.
* **Predictive Intelligence:** Implementation of classification algorithms to calculate dropout probabilities.
* **Feature Engineering:** Analysis of socioeconomic and academic variables to identify key indicators of risk.
* **Web Dashboard:** A functional interface built with **Flask** for real-time data input and prediction visualization.

##  Tech Stack
* **Language:** Python 3.9+
* **Data Science:** Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn.
* **Backend:** Flask (REST API).
* **Documentation:** Markdown & Jupyter Notebooks.

##  Project Structure
```
├── data/               # Raw and anonymized student datasets
├── models/             # Serialized trained models 
├── notebooks/          # Exploratory Data Analysis & Model Testing
├── src/                # Flask application source code
│   ├── app.py          # Main entry point
│   └── utils.py        # Data processing helpers
└── requirements.txt    # Production dependencies
```

##  Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/JeanC221/Sistema-de-Prediccion-de-Desercion-Estudiantil.git
cd Sistema-de-Prediccion-de-Desercion-Estudiantil
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the local server:**
```bash
python src/app.py
```

##  Methodology & Research
1. **Exploratory Data Analysis (EDA):** Discovered high correlation between semester progress and socioeconomic support.
2. **Model Selection:** Evaluated multiple classifiers, selecting the best performer based on Recall, to minimize false negatives in at-risk students.
3. **Deployment:** Packaged the model into a lightweight API for seamless integration with university management systems.

##  Author
**Jean Carlo Herran Rodriguez**  
Systems Engineering Student | Universidad del Norte
