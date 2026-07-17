import pandas as pd

# Load Gold data
df = pd.read_csv("data/raw/gold_h4.csv")

# Calculate EMA 50
df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()

# Calculate EMA 200
df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()

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

