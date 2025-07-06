import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import os
import unidecode

# Load and fix encoding issues
df = pd.read_csv("data/coffee_final_cleaned_no_milk.csv", sep=";", encoding="utf-8")

# Optional: clean weird encoding artifacts
def fix_encoding(text):
    if pd.isna(text): return text
    return unidecode.unidecode(str(text))

df["name"] = df["name"].map(fix_encoding)
df["brand"] = df["brand"].map(fix_encoding)
df["brand"] = df["brand"].str.lower().str.replace("'", "").str.strip()

# Drop missing values
df = df.dropna(subset=["unit_price", "quantity", "type"])

# One-hot encode coffee type
ohe = OneHotEncoder(sparse_output=False)
type_encoded = ohe.fit_transform(df[["type"]])
type_df = pd.DataFrame(type_encoded, columns=ohe.get_feature_names_out(["type"]))

# Combine features
X = pd.concat([df[["quantity"]].reset_index(drop=True), type_df], axis=1)
y = df["unit_price"].reset_index(drop=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n✅ Price Prediction Model Results:")
print(f"R² score: {r2:.2f}")
print(f"Mean Squared Error: {mse:.5f}\n")

# Plot predicted vs actual
plt.figure(figsize=(7,5))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7)
plt.xlabel("Actual Unit Price")
plt.ylabel("Predicted Unit Price")
plt.title("Actual vs Predicted Unit Prices")
plt.grid(True)
plt.tight_layout()

# Save plot
os.makedirs("img", exist_ok=True)
plt.savefig("img/actual_vs_predicted_price.png")
plt.close()