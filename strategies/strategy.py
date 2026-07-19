import pandas as pd
from config import EMA_FAST
from config import EMA_SLOW

# Load data with indicators
df = pd.read_csv("data/processed/gold_h4_with_indicators.csv")

# 🚨 SAFETY CHECK: See if ATR actually exists in the file
if "ATR_14" not in df.columns:
    print("❌ WARNING: 'ATR_14' was not found in the input file!")
    print("Make sure indicators/atr.py runs and saves to 'gold_h4_with_indicators.csv' first.")
else:
    print("✅ 'ATR_14' column successfully loaded.")

# Generate signals
df["Signal"] = ""

for i in range(1, len(df)):
    # Buy Signal
    if (
        df.loc[i, f"EMA_{EMA_FAST}"] > df.loc[i, f"EMA_{EMA_SLOW}"] and
        df.loc[i-1, f"EMA_{EMA_FAST}"] <= df.loc[i-1, f"EMA_{EMA_SLOW}"]
    ):
        df.loc[i, "Signal"] = "BUY"

    # Sell Signal
    elif (
        df.loc[i, f"EMA_{EMA_FAST}"] < df.loc[i, f"EMA_{EMA_SLOW}"] and
        df.loc[i-1, f"EMA_{EMA_FAST}"] >= df.loc[i-1, f"EMA_{EMA_SLOW}"]
    ):
        df.loc[i, "Signal"] = "SELL"

# Display only signals
signals = df[df["Signal"] != ""]

# Include ATR_14 in the printout if it exists, so we can verify it
print_cols = ["time", "close", f"EMA_{EMA_FAST}", f"EMA_{EMA_SLOW}", "RSI"]
if "ATR_14" in df.columns:
    print_cols.append("ATR_14")
print_cols.append("Signal")

print(signals[print_cols])

# Save results
df.to_csv("data/processed/gold_strategy.csv", index=False)

print("Strategy file saved successfully!")