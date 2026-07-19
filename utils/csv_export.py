import pandas as pd
from dataclasses import asdict

def save_trade_history(trade_log, output_path):
    trade_df = pd.DataFrame([asdict(t) for t in trade_log])
    trade_df.to_csv(output_path, index=False)