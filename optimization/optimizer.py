import pandas as pd
import time
from pathlib import Path

from indicators.indicator_engine import add_indicators
from indicators.atr_engine import add_atr
from strategies.strategy_engine import generate_signals

from backtesting.engine import run_backtest
from backtesting.performance import calculate_performance
from backtesting.drawdown import maximum_drawdown


BASE_DIR = Path(__file__).resolve().parent.parent

raw_data = pd.read_csv(
    BASE_DIR / "data" / "raw" / "gold_h4.csv"
)

MAX_DRAWDOWN = 15
best_profit = 0.0

split = int(len(raw_data) * 0.70)

train_df = raw_data.iloc[:split].copy()
test_df = raw_data.iloc[split:].copy()

print(f"Training candles: {len(train_df)}")
print(f"Testing candles : {len(test_df)}")

results = []

ema_fast_values = [20, 30, 40, 50]
ema_slow_values = [100, 150, 200]
atr_values = [1.0, 1.5, 2.0]
rr_values = [1.5, 2.0, 2.5, 3.0]

best_score = float("-inf")
best_params = None
best_report = None
start_time = time.time()

total_runs = (
    len(ema_fast_values)
    * len(ema_slow_values)
    * len(atr_values)
    * len(rr_values)
)

current_run = 0

def safe_profit_factor(value):
    value = str(value).strip().lower()

    if value in ("inf", "infinity"):
        return 5.0

    return float(value)

for ema_fast in ema_fast_values:
    for ema_slow in ema_slow_values:
        for atr in atr_values:
            for rr in rr_values:        

                current_run += 1
             
                df = train_df.copy()

                df = add_indicators(
                    df,
                    ema_fast=ema_fast,
                    ema_slow=ema_slow,
                )

                df = add_atr(df)

                df = generate_signals(
                    df,
                    ema_fast=ema_fast,
                    ema_slow=ema_slow,
                )

                bt = run_backtest(
                    df,
                    atr_multiplier=atr,
                    rr=rr,
                )

                report = calculate_performance(
                    bt["trade_log"],
                    bt["starting_balance"],
                    bt["balance"],
                )

                net_profit = bt["balance"] - bt["starting_balance"]

                drawdown = maximum_drawdown(
                    bt["trade_log"],
                    bt["starting_balance"],
                )

                profit_factor = safe_profit_factor(report["Profit Factor"])

                win_rate = float(
                    str(report["Win Rate"])
                    .replace("%", "")
                    .strip()
                )

                score = (
                    (net_profit / 1000)
                    * (profit_factor ** 0.5)
                    * (win_rate / 100)
                    * ((report["Total Trades"] + 10) ** 0.3)
                ) / ((drawdown + 1) ** 1.2)

                report["Score"] = round(score, 2)

                report["EMA Fast"] = ema_fast
                report["EMA Slow"] = ema_slow
                report["ATR Multiplier"] = atr
                report["Risk Reward"] = rr

                report["Net Profit Value"] = net_profit

                report["Drawdown Value"] = drawdown
                report["Maximum Drawdown"] = drawdown

                results.append(report)

                if score > best_score and drawdown < MAX_DRAWDOWN:

                    best_score = score
                    best_profit = net_profit

                    best_params = {
                        "ema_fast": ema_fast,
                        "ema_slow": ema_slow,
                        "atr": atr,
                        "rr": rr,
                    }

                    best_report = report.copy()

                    print(
                        f"⭐ New Best | "
                        f"Score={score:.2f} | "
                        f"EMA {ema_fast}/{ema_slow} | "
                        f"ATR {atr} | "
                        f"RR {rr}"
                    )

if best_params is None:
    print("No strategy met the maximum drawdown requirement.")
    exit()

print("\n===== BEST TRAINING RESULT =====")

for key, value in best_report.items():
    print(f"{key:<20}: {value}")

print("\n🏆 BEST STRATEGY")

print(f"EMA Fast : {best_params['ema_fast']}")
print(f"EMA Slow : {best_params['ema_slow']}")
print(f"ATR      : {best_params['atr']}")
print(f"RR       : {best_params['rr']}")

df = test_df.copy()

df = add_indicators(
    df,
    ema_fast=best_params["ema_fast"],
    ema_slow=best_params["ema_slow"],
)

df = add_atr(df)

df = generate_signals(
    df,
    ema_fast=best_params["ema_fast"],
    ema_slow=best_params["ema_slow"],
)

bt = run_backtest(
    df,
    atr_multiplier=best_params["atr"],
    rr=best_params["rr"],
)

test_report = calculate_performance(
    bt["trade_log"],
    bt["starting_balance"],
    bt["balance"],
)

test_drawdown = maximum_drawdown(
    bt["trade_log"],
    bt["starting_balance"],
)

test_pf = safe_profit_factor(test_report["Profit Factor"])

test_win_rate = float(
    str(test_report["Win Rate"])
    .replace("%", "")
    .strip()
)

test_score = (
    ((bt["balance"] - bt["starting_balance"]) / 1000)
    * (test_pf ** 0.5)
    * (test_win_rate / 100)
) / ((test_drawdown + 1) ** 1.2)

test_report["Score"] = round(test_score, 2)

test_report["Maximum Drawdown"] = test_drawdown

pd.DataFrame([test_report]).to_csv(
    BASE_DIR / "optimization" / "test_result.csv",
    index=False,
)

print("\n===== OUT-OF-SAMPLE TEST =====\n")

for key, value in test_report.items():
    print(f"{key:<20}: {value}")

results_df = pd.DataFrame(results)

test_score = (
    ((bt["balance"] - bt["starting_balance"]) / 1000)
    * (test_pf ** 0.5)
    * (test_win_rate / 100)
    * ((test_report["Total Trades"] + 10) ** 0.3)
) / ((test_drawdown + 1) ** 1.2)

output = (
    BASE_DIR
    / "optimization"
    / "optimization_results.csv"
)

best_strategy = pd.DataFrame([best_report])

best_strategy.drop(
    columns=["Net Profit Value", "Drawdown Value"],
    inplace=True,
)

best_strategy.to_csv(
    BASE_DIR / "optimization" / "best_strategy.csv",
    index=False,
)

results_df_to_save = results_df.drop(
    columns=["Net Profit Value", "Drawdown Value"]
)

results_df_to_save.to_csv(output, index=False)

print("\n===== TOP 10 STRATEGIES =====\n")

top10 = (
    results_df[
        [
            "EMA Fast",
            "EMA Slow",
            "ATR Multiplier",
            "Risk Reward",
            "Score",
            "Maximum Drawdown",
        ]
    ]
    .head(10)
    .reset_index(drop=True)
)

top10.index += 1

print(top10)

top10.to_csv(
    BASE_DIR / "optimization" / "top10_strategies.csv",
    index=True,
)

training_return = (
    best_profit / best_report["Starting Balance"]
) * 100

testing_return = (
    (bt["balance"] - bt["starting_balance"])
    / bt["starting_balance"]
) * 100

print(f"Training Return : {training_return:.2f}%")
print(f"Testing Return  : {testing_return:.2f}%")

if (
    testing_return > 0
    and test_drawdown <= MAX_DRAWDOWN
):
    print("Status : PASS ✅")
else:
    print("Status : FAIL ❌")

print("\n===== SUMMARY =====")

print(f"Strategies Tested : {len(results_df)}")
print(f"Training Candles  : {len(train_df)}")
print(f"Testing Candles   : {len(test_df)}")
print(f"Drawdown Limit    : {MAX_DRAWDOWN}%")
print(f"Best Score        : {best_score:.2f}")

rank = (
    results_df.reset_index(drop=True)
    .loc[
        lambda x:
            (x["EMA Fast"] == best_params["ema_fast"]) &
            (x["EMA Slow"] == best_params["ema_slow"]) &
            (x["ATR Multiplier"] == best_params["atr"]) &
            (x["Risk Reward"] == best_params["rr"])
    ]
    .index[0] + 1
)

print(f"Best Strategy Rank : {rank}/{len(results_df)}")

print(f"Saved to {output}")

print("\nScore Formula")
print(
    "(Profit/1000) × √PF × WinRate × (Trades+10)^0.3 ÷ (Drawdown+1)^1.2"
)

elapsed = time.time() - start_time

print(f"Optimization Time : {elapsed:.2f} sec")
print(f"Speed             : {total_runs / elapsed:.2f} strategies/sec")

