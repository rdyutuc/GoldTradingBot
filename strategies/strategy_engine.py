import pandas as pd


def generate_signals(df, ema_fast, ema_slow):
    fast = f"EMA_{ema_fast}"
    slow = f"EMA_{ema_slow}"

    df["Signal"] = ""

    buy = (
        (df[fast] > df[slow]) &
        (df[fast].shift(1) <= df[slow].shift(1))
    )

    sell = (
        (df[fast] < df[slow]) &
        (df[fast].shift(1) >= df[slow].shift(1))
    )

    df.loc[buy, "Signal"] = "BUY"
    df.loc[sell, "Signal"] = "SELL"

    return df