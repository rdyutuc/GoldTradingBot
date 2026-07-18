import pandas as pd
from pathlib import Path
from .trade import Trade
from .metrics import win_rate, net_profit
from .report import print_report
from dataclasses import asdict
from charts.equity_curve import plot_equity_curve

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

                trade = Trade(
                    trade_type="BUY",
                    entry_time=position["entry_time"],
                    exit_time=df.loc[i, "time"],
                    entry_price=position["entry"],
                    exit_price=position["target"],
                    stop_loss=position["stop"],
                    take_profit=position["target"],
                    result="LOSS",
                    profit=-risk,
                    balance=balance,
                    atr=df.loc[i, "ATR_14"]
                )

                trade_log.append(trade)

                position = None

            elif high >= position["target"]:

                balance += risk * RR

                wins += 1

                trade = Trade(
                    trade_type="BUY",
                    entry_time=position["entry_time"],
                    exit_time=df.loc[i, "time"],
                    entry_price=position["entry"],
                    exit_price=position["target"],
                    stop_loss=position["stop"],
                    take_profit=position["target"],
                    result="WIN",
                    profit=risk * RR,
                    balance=balance,
                    atr=df.loc[i, "ATR_14"]
                )

                trade_log.append(trade)

                position = None

        # SELL
        elif position["type"] == "SELL":

            if high >= position["stop"]:

                balance -= risk

                losses += 1

                trade = Trade(
                    trade_type="SELL",
                    entry_time=position["entry_time"],
                    exit_time=df.loc[i, "time"],
                    entry_price=position["entry"],
                    exit_price=position["stop"],
                    stop_loss=position["stop"],
                    take_profit=position["target"],
                    result="LOSS",
                    profit=-risk,
                    balance=balance,
                    atr=df.loc[i, "ATR_14"]
                )

                trade_log.append(trade)

                position = None

            elif low <= position["target"]:

                balance += risk * RR

                wins += 1

                trade = Trade(
                    trade_type="SELL",
                    entry_time=position["entry_time"],
                    exit_time=df.loc[i, "time"],
                    entry_price=position["entry"],
                    exit_price=position["target"],
                    stop_loss=position["stop"],
                    take_profit=position["target"],
                    result="WIN",
                    profit=risk * RR,
                    balance=balance,
                    atr=df.loc[i, "ATR_14"]
                )

                trade_log.append(trade)

                position = None

# -----------------------------
# Results
# -----------------------------
total = wins + losses

wr = win_rate(wins, losses) if total > 0 else 0

# -----------------------------
# Results
# -----------------------------
total = wins + losses

wr = win_rate(wins, losses) if total > 0 else 0

results = {
    "Starting Balance": f"${START_BALANCE:,.2f}",
    "Ending Balance": f"${balance:,.2f}",
    "Total Trades": total,
    "Wins": wins,
    "Losses": losses,
    "Win Rate": f"{wr:.2f}%"
}

print_report(results)

# Save trades
trade_df = pd.DataFrame([asdict(t) for t in trade_log])

output = BASE_DIR / "backtesting" / "trade_history.csv"

trade_df.to_csv(output, index=False)

print(f"\nTrade history saved to:\n{output}")

plot_equity_curve(trade_log)