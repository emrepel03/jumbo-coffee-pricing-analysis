import pandas as pd
import unidecode

# Load your existing strict cleaned data
df = pd.read_csv("data/coffee_final_cleaned_strict.csv", sep=";")

# Extract brand (first word of product name) if brand column does not exist
if "brand" not in df.columns:
    df["brand"] = df["name"].str.split().str[0]

# Normalize brand names:
# 1. Lowercase
# 2. Remove accents (like trema)
df["brand"] = df["brand"].str.lower().apply(unidecode.unidecode)

# Filter out common meaningless brand-like words
remove_brands = {"van", "de", "het", "en", "coffee", "koffie", "the", "by", "voor", "met", "aan"}

df = df[~df["brand"].isin(remove_brands)]

# Optional: You can also fix known common misspellings manually, e.g.
df["brand"] = df["brand"].replace({
    "nescafe": "nescafé",
    "illy": "illy",
    "starbucks": "starbucks"
})

# Save the updated CSV
df.to_csv("data/coffee_final_cleaned_normalized.csv", index=False, sep=";")

print("✅ Saved normalized brand data to coffee_final_cleaned_normalized.csv")