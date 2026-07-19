import pandas as pd

# Load Gold data
df = pd.read_csv("data/raw/gold_h4.csv")

# Calculate EMA
ema_periods = [20, 30, 50, 100, 150, 200]

for period in ema_periods:
    df[f"EMA_{period}"] = (
        df["close"]
        .ewm(span=period, adjust=False)
        .mean()
    )

# Calculate RSI  (14)
delta = df['close'].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()

rs = avg_gain / avg_loss

df['RSI'] = 100 - (100 / (1 + rs))

# Display the latest rows
print(df[['time', 'close', 'EMA_50', 'EMA_200', 'RSI']].tail())

# Save the updated data
df.to_csv("data/processed/gold_h4_with_indicators.csv", index=False)

print("Indicators calculated successfully!")

