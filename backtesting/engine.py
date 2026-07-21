import pandas as pd
from .trade import Trade


def run_backtest(
    df,
    starting_balance=10000,
    risk_percent=1,
    atr_multiplier=1.5,
    rr=2,
):
    
    START_BALANCE = starting_balance
    RISK_PERCENT = risk_percent
    ATR_MULTIPLIER = atr_multiplier
    RR = rr

    # -----------------------------
    # Variables
    # -----------------------------
    balance = START_BALANCE

    wins = 0
    losses = 0

    trade_log = []

    position = None

    # -----------------------------
# Backtest
# -----------------------------
    for i in range(20, len(df) - 1):

        # Skip rows with no ATR yet
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        if pd.isna(row["ATR_14"]):
            continue

        # -------------------------
        # Open new trade
        # -------------------------
        if position is None:

            signal = row["Signal"]

            if signal == "BUY":

                entry = next_row["open"]

                stop = entry - ATR_MULTIPLIER * row["ATR_14"]

                target = entry + (entry - stop) * RR

                position = {
                    "type": "BUY",
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "entry_time": next_row["time"]
                }

            elif signal == "SELL":

                entry = next_row["open"]

                stop = entry + ATR_MULTIPLIER * row["ATR_14"]

                target = entry - (stop - entry) * RR

                position = {
                    "type": "SELL",
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "entry_time": next_row["time"]
                }

        # -------------------------
        # Manage open trade
        # -------------------------
        else:

            high = row["high"]
            low = row["low"]

            risk = balance * RISK_PERCENT / 100

            # BUY
            if position["type"] == "BUY":

                if low <= position["stop"]:

                    balance -= risk

                    losses += 1

                    trade = Trade(
                        trade_type="BUY",
                        entry_time=position["entry_time"],
                        exit_time=row["time"],
                        entry_price=position["entry"],
                        exit_price=position["target"],
                        stop_loss=position["stop"],
                        take_profit=position["target"],
                        result="LOSS",
                        profit=-risk,
                        balance=balance,
                        atr=row["ATR_14"]
                    )

                    trade_log.append(trade)

                    position = None

                elif high >= position["target"]:

                    balance += risk * RR

                    wins += 1

                    trade = Trade(
                        trade_type="BUY",
                        entry_time=position["entry_time"],
                        exit_time=row["time"],
                        entry_price=position["entry"],
                        exit_price=position["target"],
                        stop_loss=position["stop"],
                        take_profit=position["target"],
                        result="WIN",
                        profit=risk * RR,
                        balance=balance,
                        atr=row["ATR_14"]
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
                        exit_time=row["time"],
                        entry_price=position["entry"],
                        exit_price=position["stop"],
                        stop_loss=position["stop"],
                        take_profit=position["target"],
                        result="LOSS",
                        profit=-risk,
                        balance=balance,
                        atr=row["ATR_14"]
                    )

                    trade_log.append(trade)

                    position = None

                elif low <= position["target"]:

                    balance += risk * RR

                    wins += 1

                    trade = Trade(
                        trade_type="SELL",
                        entry_time=position["entry_time"],
                        exit_time=row["time"],
                        entry_price=position["entry"],
                        exit_price=position["target"],
                        stop_loss=position["stop"],
                        take_profit=position["target"],
                        result="WIN",
                        profit=risk * RR,
                        balance=balance,
                        atr=row["ATR_14"]
                    )

                    trade_log.append(trade)

                    position = None

    return {
        "starting_balance": START_BALANCE,
        "balance": balance,
        "wins": wins,
        "losses": losses,
        "trade_log": trade_log,
    }