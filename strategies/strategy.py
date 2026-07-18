import pandas as pd

# Load data with indicators
df = pd.read_csv("data/processed/gold_h4_with_indicators.csv")

# Generate signals
df["Signal"] = ""

for i in range(1, len(df)):
    # Buy Signal
    if (
        df.loc[i, "EMA_50"] > df.loc[i, "EMA_200"] and
        df.loc[i-1, "EMA_50"] <= df.loc[i-1, "EMA_200"]
    ):
        df.loc[i, "Signal"] = "BUY"

    # Sell Signal
    elif (
        df.loc[i, "EMA_50"] < df.loc[i, "EMA_200"] and
        df.loc[i-1, "EMA_50"] >= df.loc[i-1, "EMA_200"]
    ):
        df.loc[i, "Signal"] = "SELL"

# Display only signals
signals = df[df["Signal"] != ""]

print(signals[["time", "close", "EMA_50", "EMA_200", "RSI","Signal"]])

# Save results
df.to_csv("data/processed/gold_strategy.csv", index=False)

print("Strategy file saved successfully!")