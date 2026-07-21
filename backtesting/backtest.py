import pandas as pd
from pathlib import Path
from .engine import run_backtest
from utils.csv_export import save_trade_history
from .report import print_report
from .drawdown import maximum_drawdown
from .performance import calculate_performance
from charts.equity_curve import plot_equity_curve


# -----------------------------
# Load Data
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "data" / "processed" / "gold_strategy.csv"
)

engine_results = run_backtest(df)

balance = engine_results["balance"]
wins = engine_results["wins"]
losses = engine_results["losses"]
trade_log = engine_results["trade_log"]
START_BALANCE = engine_results["starting_balance"]


# -----------------------------
# Results
# -----------------------------
report = calculate_performance(
    trade_log,
    START_BALANCE,
    balance
)

report["Maximum Drawdown"] = maximum_drawdown(
    trade_log,
    START_BALANCE,
)

print_report(report)

# Save trades
output = BASE_DIR / "backtesting" / "trade_history.csv"

save_trade_history(trade_log, output)

print(f"\nTrade history saved to:\n{output}")

plot_equity_curve(trade_log)