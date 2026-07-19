import pandas as pd

from config import EMA_FAST, EMA_SLOW, RSI_PERIOD
from indicators.indicator_engine import add_indicators

# Load raw data
df = pd.read_csv("data/raw/gold_h4.csv")

# Add indicators
df = add_indicators(
    df,
    ema_fast=EMA_FAST,
    ema_slow=EMA_SLOW,
    rsi_period=RSI_PERIOD,
)

# Save
df.to_csv(
    "data/processed/gold_h4_with_indicators.csv",
    index=False,
)

print("Indicators calculated successfully!")