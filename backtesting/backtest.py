import pandas as pd
from pathlib import Path

# -----------------------------
# Load Data
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data" / "processed" / "gold_strategy.csv")

# -----------------------------
# Settings
# -----------------------------
START_BALANCE = 10000
RISK_PERCENT = 1
ATR_MULTIPLIER = 1.5
RR = 2

balance = START_BALANCE

wins = 0
losses = 0

trade_log = []

position = None

# -----------------------------
# Backtest
# -----------------------------
for i in range(20, len(df)):

    # Skip rows with no ATR yet
    if pd.isna(df.loc[i, "ATR_14"]):
        continue

    # -------------------------
    # Open new trade
    # -------------------------
    if position is None:

        signal = df.loc[i, "Signal"]

        if signal == "BUY":

            entry = df.loc[i + 1, "open"]

            stop = entry - ATR_MULTIPLIER * df.loc[i, "ATR_14"]

            target = entry + (entry - stop) * RR

            position = {
                "type": "BUY",
                "entry": entry,
                "stop": stop,
                "target": target,
                "entry_time": df.loc[i + 1, "time"]
            }

        elif signal == "SELL":

            entry = df.loc[i + 1, "open"]

            stop = entry + ATR_MULTIPLIER * df.loc[i, "ATR_14"]

            target = entry - (stop - entry) * RR

            position = {
                "type": "SELL",
                "entry": entry,
                "stop": stop,
                "target": target,
                "entry_time": df.loc[i + 1, "time"]
            }

    # -------------------------
    # Manage open trade
    # -------------------------
    else:

        high = df.loc[i, "high"]
        low = df.loc[i, "low"]

        risk = balance * RISK_PERCENT / 100

        # BUY
        if position["type"] == "BUY":

            if low <= position["stop"]:

                balance -= risk

                losses += 1

                trade_log.append({
                    "Type": "BUY",
                    "Result": "LOSS",
                    "Entry": position["entry"],
                    "Exit": position["stop"],
                    "Balance": balance
                })

                position = None

            elif high >= position["target"]:

                balance += risk * RR

                wins += 1

                trade_log.append({
                    "Type": "BUY",
                    "Result": "WIN",
                    "Entry": position["entry"],
                    "Exit": position["target"],
                    "Balance": balance
                })

                position = None

        # SELL
        elif position["type"] == "SELL":

            if high >= position["stop"]:

                balance -= risk

                losses += 1

                trade_log.append({
                    "Type": "SELL",
                    "Result": "LOSS",
                    "Entry": position["entry"],
                    "Exit": position["stop"],
                    "Balance": balance
                })

                position = None

            elif low <= position["target"]:

                balance += risk * RR

                wins += 1

                trade_log.append({
                    "Type": "SELL",
                    "Result": "WIN",
                    "Entry": position["entry"],
                    "Exit": position["target"],
                    "Balance": balance
                })

                position = None

# -----------------------------
# Results
# -----------------------------
total = wins + losses

win_rate = (wins / total * 100) if total > 0 else 0

print("=" * 45)
print("BACKTEST VERSION 2")
print("=" * 45)
print(f"Starting Balance : ${START_BALANCE:,.2f}")
print(f"Ending Balance   : ${balance:,.2f}")
print(f"Total Trades     : {total}")
print(f"Wins             : {wins}")
print(f"Losses           : {losses}")
print(f"Win Rate         : {win_rate:.2f}%")

# Save trades
trade_df = pd.DataFrame(trade_log)

output = BASE_DIR / "backtesting" / "trade_history.csv"

trade_df.to_csv(output, index=False)

print(f"\nTrade history saved to:\n{output}")