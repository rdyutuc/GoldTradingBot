import pandas as pd

from config import EMA_FAST, EMA_SLOW
from strategies.strategy_engine import generate_signals

# Load data
df = pd.read_csv("data/processed/gold_h4_with_indicators.csv")

# Safety check
if "ATR_14" not in df.columns:
    print("❌ WARNING: ATR_14 not found.")
    exit()

print("✅ ATR_14 column loaded.")

# Generate signals
df = generate_signals(
    df,
    ema_fast=EMA_FAST,
    ema_slow=EMA_SLOW,
)

# Show signals
signals = df[df["Signal"] != ""]

print_cols = [
    "time",
    "close",
    f"EMA_{EMA_FAST}",
    f"EMA_{EMA_SLOW}",
    "RSI",
    "ATR_14",
    "Signal",
]

print(signals[print_cols])

# Save
df.to_csv(
    "data/processed/gold_strategy.csv",
    index=False,
)

print("Strategy file saved successfully!")