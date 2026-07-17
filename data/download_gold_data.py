import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# Connect to MT5
if not mt5.initialize():
    print("Failed to connect:", mt5.last_error())
    quit()

symbol = "XAUUSDm"

# Make sure the symbol is available
if not mt5.symbol_select(symbol, True):
    print(f"Could not select {symbol}")
    mt5.shutdown()
    quit()

# Get the latest 1000 H4 candles
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 1000)

# Convert to DataFrame
df = pd.DataFrame(rates)

# Convert Unix time to readable date/time
df['time'] = pd.to_datetime(df['time'], unit='s')

print(df.head())
print(df.tail())

# Save to CSV
df.to_csv("data/processed/gold_h4_with_indicators.csv", index=False)

print("Saved data to gold_h4.csv")

mt5.shutdown()