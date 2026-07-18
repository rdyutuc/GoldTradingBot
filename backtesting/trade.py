from dataclasses import dataclass


@dataclass
class Trade:
    trade_type: str
    entry_time: str
    exit_time: str

    entry_price: float
    exit_price: float

    stop_loss: float
    take_profit: float

    result: str

    profit: float

    balance: float

    atr: float