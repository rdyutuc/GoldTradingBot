import pandas as pd


def generate_signals(df, ema_fast, ema_slow):
    """
    Generate BUY/SELL signals based on EMA crossover.
    """

    df["Signal"] = ""

    for i in range(1, len(df)):

        # BUY
        if (
            df.loc[i, f"EMA_{ema_fast}"] > df.loc[i, f"EMA_{ema_slow}"]
            and
            df.loc[i - 1, f"EMA_{ema_fast}"] <= df.loc[i - 1, f"EMA_{ema_slow}"]
        ):
            df.loc[i, "Signal"] = "BUY"

        # SELL
        elif (
            df.loc[i, f"EMA_{ema_fast}"] < df.loc[i, f"EMA_{ema_slow}"]
            and
            df.loc[i - 1, f"EMA_{ema_fast}"] >= df.loc[i - 1, f"EMA_{ema_slow}"]
        ):
            df.loc[i, "Signal"] = "SELL"

    return df