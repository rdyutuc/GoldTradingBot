import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
input_file = BASE_DIR / "data" / "processed" / "gold_h4_with_indicators.csv"
output_file = BASE_DIR / "data" / "processed" / "gold_h4_with_indicators.csv"

# Read data
df = pd.read_csv(input_file)

# Calculate True Range
df["H-L"] = df["high"] - df["low"]
df["H-PC"] = abs(df["high"] - df["close"].shift(1))
df["L-PC"] = abs(df["low"] - df["close"].shift(1))

df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)

# ATR (14)
df["ATR_14"] = df["TR"].rolling(window=14).mean()

# Remove temporary columns
df.drop(columns=["H-L", "H-PC", "L-PC", "TR"], inplace=True)

# Save
df.to_csv("data/processed/gold_strategy.csv", index=False)

print("✅ ATR calculated successfully!")