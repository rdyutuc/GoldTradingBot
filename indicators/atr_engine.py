import pandas as pd


def add_atr(df, period=14):
    """
    Add Average True Range (ATR) to a DataFrame.
    """

    # True Range
    df["H-L"] = df["high"] - df["low"]
    df["H-PC"] = (df["high"] - df["close"].shift(1)).abs()
    df["L-PC"] = (df["low"] - df["close"].shift(1)).abs()

    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)

    # ATR
    df[f"ATR_{period}"] = df["TR"].rolling(window=period).mean()

    # Remove temporary columns
    df.drop(
        columns=["H-L", "H-PC", "L-PC", "TR"],
        inplace=True,
    )

    return df