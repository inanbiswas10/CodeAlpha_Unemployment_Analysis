# 📈 National Unemployment & COVID-19 Shock Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0%2B-3F4F75.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive industrial grade data science application for analyzing workforce trends, regional unemployment disparities and COVID-19 pandemic shocks across Indian states.

Developed as part of the **CodeAlpha Data Science Internship Program**.

---

## 🌐 Live Application

Access the production dashboard live on Streamlit Cloud:  

👉 **[https://national-unemployment-analytics-platform.streamlit.app/](https://national-unemployment-analytics-platform.streamlit.app/)**

---

## 📑 Table of Contents

- [Live Demo](#-national-unemployment--covid-19-shock-analytics-platform)
- [Key Features](#-key-features)
- [Repository Architecture](#-repository-architecture)
- [Dataset](#-dataset)
- [Local Installation & Setup](#-local-installation--setup)
- [Automated Testing](#-automated-testing)
- [Tech Stack](#️-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Author](#-author)

---

## 🌟 Key Features

- **📉 Interactive Time-Series Analytics** — Multi-state trend inspection with COVID-19 lockdown periods highlighted directly on the timeline.
- **🗺️ Geospatial Severity Heatmaps** — Mapbox-powered bubble maps rendering state-by-state unemployment intensity.
- **🏛️ Macro-Zone Distribution Analysis** — Boxplot and distribution breakdowns comparing North, South, East, West and Northeast economic zones.
- **⚡ COVID-19 Impact Matrix** — State-level vulnerability ranking quantifying pre-lockdown vs peak-lockdown unemployment rate spikes.
- **🔮 Predictive Trend Forecasting** — Polynomial regression engine projecting short-term post-lockdown unemployment trajectories with a dynamic horizon slider.
- **📊 Correlation & Anomaly Detection** — Pearson correlation heatmaps and Z-score outlier detection for isolating statistical anomalies.
- **📋 Automated Executive Briefing** — Dynamic textual summary of key COVID-19 impact findings and strategic policy recommendations.
- **📥 CSV Data Export** — Download filtered analytical views directly from the sidebar for offline research.

---

## 📂 Repository Architecture

```text
CodeAlpha_Unemployment_Analysis/
├── .streamlit/
│   └── config.toml          # Custom dark UI theme configuration
├── app/
│   └── main.py               # Core Streamlit web application frontend
├── data/
│   ├── Unemployment in India.csv
│   └── Unemployment_Rate_upto_11_2020.csv
├── src/
│   ├── analytics.py          # Statistical algorithms, ML forecasting & Z-score engines
│   └── data_loader.py        # Data cleaning, normalization & coordinate mapping
├── tests/
│   └── test_analytics.py     # Automated pytest verification suite
├── requirements.txt           # Production dependencies
└── README.md                  # Project documentation
```

---

## 🧮 Dataset

The dashboard combines two publicly available Indian unemployment datasets stored under `data/`:

| File | Description |
|---|---|
| `Unemployment in India.csv` | Regional unemployment, employment, and labor participation figures across Indian states and UTs. |
| `Unemployment_Rate_upto_11_2020.csv` | Monthly unemployment and labor participation rates through November 2020, including state-level latitude/longitude used for the geospatial heatmaps. |

Cleaning, normalization and coordinate mapping logic lives in `src/data_loader.py`.

---

## 🚀 Local Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/inanbiswas10/CodeAlpha_Unemployment_Analysis.git
cd CodeAlpha_Unemployment_Analysis
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Web Application

```bash
streamlit run app/main.py
```

---

## 🔬 Automated Testing

Run the automated pytest verification suite:

```bash
pytest tests/
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| Visualization | Plotly Express, Plotly Graph Objects |
| Data Processing & Analytics | Pandas, NumPy, SciPy |
| Machine Learning | Scikit-Learn |

---

## 🤝 Contributing

This project was built as part of a data science internship but suggestions, bug reports and pull requests are welcome. Feel free to open an issue if you spot something that could be improved.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **CodeAlpha** — for the Data Science Internship Program and project guidance.
- The open unemployment datasets that made this analysis possible.

---

## 👤 Author

**Inan Biswas**

- GitHub: [@inanbiswas10](https://github.com/inanbiswas10)
- LinkedIn: [inanbiswas10](https://www.linkedin.com/in/inanbiswas10)

---

⭐ If you find this project useful, consider giving it a star !!