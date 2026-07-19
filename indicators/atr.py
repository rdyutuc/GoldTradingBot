import pandas as pd

from indicators.atr_engine import add_atr

# Load file
df = pd.read_csv("data/processed/gold_h4_with_indicators.csv")

# Calculate ATR
df = add_atr(df)

# Save
df.to_csv(
    "data/processed/gold_h4_with_indicators.csv",
    index=False,
)

print("✅ ATR calculated successfully!")