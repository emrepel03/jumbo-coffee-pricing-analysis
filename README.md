A data science project investigating coffee product pricing using web scraping, clustering, SQL, and ML — presented through an interactive dashboard.

# ☕ Jumbo Coffee Pricing Analysis

**Explore how coffee prices vary across types and brands in Dutch supermarkets.**  
An end-to-end data science project with real scraping, EDA, clustering, ML, and an interactive dashboard.

🔗 Try the Dashboard Live: [Streamlit App][(https://jumbo-coffee-pricing-analysis-gnel9nyvr3dtdbcasxclh9.streamlit.app/)]

---

## 🚀 Project Highlights

✅ **Real-World Problem**: Price transparency in grocery markets using coffee products as a use case  
✅ **End-to-End Pipeline**: From web scraping to visualization and prediction  
✅ **Skills Demonstrated**:
- Data Cleaning & Wrangling
- EDA & Statistical Visualization (Seaborn, Matplotlib)
- Clustering (KMeans)
- Machine Learning (Linear Regression)
- Dashboard Development (Streamlit)
- Modular Python Codebase
- SQL analysis on product pricing (via SQLite)

---

## 🗂️ Project Structure

```
📁 jumbo-coffee-pricing-analysis
├── data/                          # Cleaned dataset (CSV)
├── dashboard/                     # Streamlit dashboard app
├── img/                           # Saved plots for reporting or presentation
├── scraper.py                     # Custom web scraper
├── clean_data.py                  # Data cleaning script
├── normalize_brands.py            # Brand name normalization
├── cluster_analysis.py            # KMeans clustering logic
├── price_prediction_model.py      # Linear regression model
├── sql_analysis.py                # SQL querying for analytical insights
├── requirements.txt               # Python dependencies
└── README.md                      # Project overview
```

---

## 📊 Dashboard Features

✅ **Filter by coffee type, brand, and price range**  
✅ **Interactive plots**:  
- Price distribution  
- Cheapest and most expensive brands & products  
- Average price by type  
- Clustering by quantity & price  
✅ **Data export**: Download filtered datasets with one click  
✅ **Live ML summary**: Model info (R² score, MSE) with interpretation

To run:
```bash
pip install -r requirements.txt
streamlit run dashboard/coffee_dashboard.py
```

---

## 🔍 Data Overview

- **Source**: Scraped from real Dutch supermarket websites (e.g., Jumbo)
- **Variables**: `name`, `brand`, `type`, `price`, `quantity`, `unit_price`
- **Unit Price Standardized**: Per gram or capsule for fair comparison

---

## 📈 Sample Insights

- **Illy** dominates high-end coffee pricing  
- **Melitta** and **Perla** offer budget options  
- **Capsules** are significantly more expensive per gram than beans  
- Clustering reveals 3 distinct product-price segments  

---

## 🧠 ML Summary

- **Model**: Linear Regression  
- **Features**: Quantity, Type  
- **Target**: Unit Price  
- **Performance**:  
  - R² Score: 0.34  
  - MSE: 0.00017  
- **Interpretation**: Explains pricing partially — other hidden factors likely affect prices

---

## 🧾 SQL Analysis

This project also includes SQL-based analysis using SQLite to explore product pricing patterns and perform custom queries. This highlights familiarity with databases and structured querying in a data science workflow.

---

## 👨‍💻 Author

**Emre Pelzer**  
Bachelor of Data Science & AI  
Maastricht University  
📫 [LinkedIn](https://www.linkedin.com/in/emre-pelzer-b14148324) | [GitHub](https://github.com/emrepel03)

---

## 🏁 Final Words

This project is designed to demonstrate my readiness for real-world data roles — showcasing not just code and models, but complete end-to-end thinking. I would love to discuss this further in an interview.