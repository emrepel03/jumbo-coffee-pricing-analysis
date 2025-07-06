import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import os
import unidecode

df = pd.read_csv("data/coffee_final_cleaned_no_milk.csv", sep=";", encoding="utf-8")

def clean_text(s):
    if pd.isna(s): return s
    return unidecode.unidecode(s)

df["name"] = df["name"].astype(str).map(clean_text)
df["brand"] = df["brand"].astype(str).map(clean_text)
df["brand"] = df["brand"].str.lower().str.replace("'", "").str.strip()

df = df.dropna(subset=["unit_price", "quantity"])

df["quantity_norm"] = df["quantity"] / df["quantity"].max()

X = df[["unit_price", "quantity_norm"]]

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="unit_price", y="quantity_norm", hue="cluster", palette="Set2", s=80)
plt.title("Clustering of Coffee Products by Unit Price and Quantity")
plt.xlabel("Unit Price (€ per gram/ml)")
plt.ylabel("Quantity (normalized)")
plt.tight_layout()

os.makedirs("img", exist_ok=True)
plt.savefig("img/cluster_price_quantity.png")
print("✅ Clustering plot saved to img/cluster_price_quantity.png")