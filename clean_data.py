import pandas as pd
import csv

# Load the raw scraped data
df = pd.read_csv("data/jumbo_prices.csv", sep=";")

# Convert price column to numeric
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Remove duplicates based on name and price 
before = len(df)
df = df.drop_duplicates(subset=["name", "price"])
after = len(df)
print(f"🧹 Removed {before - after} duplicates")

# Normalize brand: lowercase, strip spaces, extract first word as brand
df["brand"] = df["name"].str.lower().str.strip().str.split().str[0]

# Remove invalid brands / stopwords (adjust this set as needed)
invalid_brands = {"van", "coffee", "koffie", "the", "and", "by", "of", "de", "la", "le"}
before_brand = len(df)
df = df[~df["brand"].isin(invalid_brands)]
after_brand = len(df)
print(f"🧹 Removed {before_brand - after_brand} rows with invalid brands")

# Save cleaned data
df.to_csv("data/jumbo_prices_clean.csv", index=False, sep=';', quoting=csv.QUOTE_MINIMAL)
print("✅ Saved cleaned data:", len(df), "products")