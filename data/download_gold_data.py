import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# -----------------------------
# Connect to MT5
# -----------------------------
if not mt5.initialize():
    print("Failed to connect:", mt5.last_error())
    quit()

symbol = "XAUUSDm"

if not mt5.symbol_select(symbol, True):
    print(f"Could not select {symbol}")
    mt5.shutdown()
    quit()

# -----------------------------
# Download 5 years of H4 data
# -----------------------------
start_date = datetime(2021, 1, 1)
end_date = datetime.now()

rates = mt5.copy_rates_range(
    symbol,
    mt5.TIMEFRAME_H4,
    start_date,
    end_date
)

if rates is None:
    print("Failed to download data.")
    mt5.shutdown()
    quit()

# -----------------------------
# Convert to DataFrame
# -----------------------------
df = pd.DataFrame(rates)

df["time"] = pd.to_datetime(df["time"], unit="s")

print(df.head())
print(df.tail())

print(f"\nDownloaded {len(df)} candles.")

# -----------------------------
# Save
# -----------------------------
df.to_csv(
    "data/raw/gold_h4.csv",
    index=False
)

print("Gold data saved successfully!")

mt5.shutdown()