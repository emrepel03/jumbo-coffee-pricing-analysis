import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import unidecode
from matplotlib.lines import Line2D

# Configure page
st.set_page_config(page_title="Coffee Market Dashboard", layout="wide")
st.markdown("<style>.block-container { padding-top: 2rem; }</style>", unsafe_allow_html=True)

# Set global font sizes for plots
plt.rcParams.update({
    'font.size': 4,
    'axes.titlesize': 4,
    'axes.labelsize': 3.5,
    'xtick.labelsize': 3,
    'ytick.labelsize': 3,
    'legend.fontsize': 3
})

# Load data
df = pd.read_csv("data/coffee_final_cleaned_no_milk.csv", sep=";", encoding="latin1")
df["name"] = df["name"].astype(str).apply(unidecode.unidecode)
df["type"] = df["type"].astype(str).apply(unidecode.unidecode).str.strip()
df = df[df["type"].notna() & (df["type"].str.lower() != "nan")]

st.sidebar.markdown(f"**Total Products:** {len(df)}")
st.sidebar.markdown("**Type Breakdown:**")
for t, count in df["type"].value_counts().items():
    st.sidebar.markdown(f"- {t}: {count}")

st.sidebar.header("🔍 Filters")
coffee_types_clean = df["type"].dropna().astype(str).apply(str.strip)
coffee_types = ["All"] + sorted(coffee_types_clean.unique(), key=str.lower)
selected_type = st.sidebar.selectbox("Select Coffee Type", coffee_types)
brands = ["All"] + sorted(df["brand"].dropna().unique(), key=str.lower)
selected_brand = st.sidebar.selectbox("Select Brand", brands)

price_min, price_max = float(df["unit_price"].min()), float(df["unit_price"].max())
price_range = st.sidebar.slider(
    "Unit Price Range (EUR)",
    price_min, price_max, (price_min, price_max)
)

# Filtered Data
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]
if selected_brand != "All":
    filtered_df = filtered_df[filtered_df["brand"] == selected_brand]
filtered_df = filtered_df[(filtered_df["unit_price"] >= price_range[0]) & (filtered_df["unit_price"] <= price_range[1])]

st.title("🍵 JUMBO Supermarket Coffee Insights Dashboard")

st.subheader(f"📊 Filtered Products: {len(filtered_df)} items")
st.dataframe(filtered_df[["name", "type", "brand", "unit_price"]].sort_values("unit_price"), use_container_width=True)

# Summary Stats
st.subheader("🤔 Summary: Unit Price by Coffee Type")
sum_stats = filtered_df.groupby("type")["unit_price"].agg(["mean", "min", "max"]).reset_index()
sum_stats.columns = ["Coffee Type", "Avg Price", "Min Price", "Max Price"]
st.table(sum_stats.style.format({"Avg Price": "{:.4f}", "Min Price": "{:.4f}", "Max Price": "{:.4f}"}))

# Plot: Pie chart of coffee type distribution
st.subheader("☕ Coffee Type Distribution")
st.markdown("This chart shows the distribution of coffee types in the filtered products.")
type_counts = filtered_df["type"].value_counts()
fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
wedges, texts, autotexts = ax_pie.pie(
    type_counts, labels=type_counts.index, autopct="%1.1f%%", startangle=90,
    textprops={'fontsize': 7}
)
ax_pie.set_title("Distribution of Coffee Types", fontsize=4)
for text in texts + autotexts:
    text.set_fontsize(5)
st.pyplot(fig_pie)

# Plot: Avg Price by Type
st.subheader("📊 Avg Unit Price by Type")
st.markdown("This chart shows the average unit price for each coffee type.")
fig1, ax1 = plt.subplots(figsize=(2.5, 1.5))
sns.barplot(
    data=filtered_df,
    x="type", y="unit_price",
    estimator="mean", errorbar=None,
    palette="pastel", ax=ax1,
    order=filtered_df.groupby("type")["unit_price"].mean().sort_values(ascending=False).index
)
ax1.set_title("Average Price by Coffee Type")
ax1.set_ylabel("Unit Price (EUR)")
ax1.tick_params(axis='x', rotation=45)
for container in ax1.containers:
    ax1.bar_label(container, fmt="%.2f", label_type="edge", fontsize=3)
st.pyplot(fig1)

# Plot: Top 10 Expensive Brands
st.subheader("🔹 Top 10 Most Expensive Brands")
st.markdown("This chart identifies the 10 brands with the highest average unit price.")
top_brands = filtered_df.groupby("brand")["unit_price"].mean().nlargest(10).reset_index()
fig2, ax2 = plt.subplots(figsize=(2.5, 1.5))
sns.barplot(data=top_brands, x="unit_price", y="brand", palette="Reds", ax=ax2)
for container in ax2.containers:
    ax2.bar_label(container, fmt="%.2f", label_type="edge", fontsize=3)
ax2.set_title("Most Expensive Brands by Avg Unit Price")
ax2.set_xlabel("Unit Price (EUR)")
ax2.set_ylabel("Brand")
st.pyplot(fig2)

# Plot: Top 10 Cheapest Brands
st.subheader("✅ Top 10 Cheapest Brands")
st.markdown("This chart shows the 10 brands with the lowest average unit price.")
cheap_brands = filtered_df.groupby("brand")["unit_price"].mean().nsmallest(10).reset_index()
fig3, ax3 = plt.subplots(figsize=(2.5, 1.5))
sns.barplot(data=cheap_brands, x="unit_price", y="brand", palette="Greens", ax=ax3)
for container in ax3.containers:
    ax3.bar_label(container, fmt="%.2f", label_type="edge", fontsize=3)
ax3.set_title("Cheapest Brands by Avg Unit Price")
ax3.set_xlabel("Unit Price (EUR)")
ax3.set_ylabel("Brand")
st.pyplot(fig3)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 💰 Cheapest Brands")
    st.table(cheap_brands[["brand", "unit_price"]].round(3).reset_index(drop=True))
with col2:
    st.markdown("#### 💸 Most Expensive Brands")
    st.table(top_brands[["brand", "unit_price"]].round(3).reset_index(drop=True))

# Plot: Distribution
st.subheader("📈 Distribution of Unit Prices")
st.markdown("This histogram shows the distribution of unit prices among the filtered products.")
fig4, ax4 = plt.subplots(figsize=(2.5, 1.5))
sns.histplot(filtered_df["unit_price"], bins=30, kde=True, color="skyblue", ax=ax4)
ax4.set_xlabel("Unit Price (EUR)")
ax4.set_title("Distribution of Unit Prices")
st.pyplot(fig4)

# Plot: Clustering (KMeans)
st.subheader("🧰 Clustering Coffee by Quantity & Price")
st.markdown("This scatterplot clusters products based on quantity and unit price to reveal pricing patterns.")
cluster_df = filtered_df.dropna(subset=["quantity", "unit_price"]).copy()
if len(cluster_df) > 0:
    cluster_df["log_quantity"] = np.log1p(cluster_df["quantity"])
    X = cluster_df[["log_quantity", "unit_price"]]
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_df["cluster"] = kmeans.fit_predict(X) + 1

    # Define custom colors
    cluster_colors = {1: "#66c2a5", 2: "#fc8d62", 3: "#8da0cb"}
    colors = cluster_df["cluster"].map(cluster_colors)

    fig5, ax5 = plt.subplots(figsize=(5, 3))
    scatter = ax5.scatter(
        cluster_df["quantity"], cluster_df["unit_price"],
        c=colors, alpha=0.7, s=15
    )
    ax5.set_xlabel("Quantity (grams or count)")
    ax5.set_ylabel("Unit Price (EUR)")
    ax5.set_title("KMeans Clustering")

    ax5.title.set_fontsize(10)
    ax5.xaxis.label.set_fontsize(9)
    ax5.yaxis.label.set_fontsize(9)
    ax5.tick_params(axis='both', labelsize=8)

    # Always show legend in order Cluster 1, Cluster 2, Cluster 3
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Cluster 1', markerfacecolor=cluster_colors[1], markersize=5),
        Line2D([0], [0], marker='o', color='w', label='Cluster 2', markerfacecolor=cluster_colors[2], markersize=5),
        Line2D([0], [0], marker='o', color='w', label='Cluster 3', markerfacecolor=cluster_colors[3], markersize=5),
    ]
    ax5.legend(handles=legend_elements, title="Cluster", loc="upper right", fontsize=3, title_fontsize=3.5)
    st.pyplot(fig5)

    ccounts = cluster_df["cluster"].value_counts().sort_index()
    st.markdown("**Cluster Sizes**: " + ", ".join(f"Cluster {i}: {c}" for i, c in ccounts.items()))
else:
    st.warning("Not enough data for clustering.")

# Optional: Price Prediction Model Result (Summary only)
st.subheader("🔢 Price Prediction (Model Summary)")
st.markdown("""
- **Model**: Linear Regression  
- **Features**: Quantity, Type  
- **Target**: Unit Price  
- **R² Score**: 0.34  
- **MSE**: 0.00017  
Note: Unit Price is standardized per gram or capsule to ensure fair comparison across product types.
""")

# Download button
st.subheader("📂 Download Filtered Data")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False, sep=";"),
    file_name="coffee_filtered.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown("Built by Emre Pelzer | [GitHub](https://github.com/emrepel03)", unsafe_allow_html=True)