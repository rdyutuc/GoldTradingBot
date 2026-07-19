import pandas as pd


def add_indicators(
    df,
    ema_fast=50,
    ema_slow=200,
    rsi_period=14
):
    """
    Add EMA and RSI indicators to a DataFrame.
    """

    # EMA
    df[f"EMA_{ema_fast}"] = (
        df["close"]
        .ewm(span=ema_fast, adjust=False)
        .mean()
    )

    df[f"EMA_{ema_slow}"] = (
        df["close"]
        .ewm(span=ema_slow, adjust=False)
        .mean()
    )

    # RSI
    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(rsi_period).mean()

    avg_loss = loss.rolling(rsi_period).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    return df