import subprocess
import sys

python = sys.executable

print("Step 1: Downloading Gold data...")
subprocess.run([python, "data/download_gold_data.py"], check=True)

print("Step 2: Calculating indicators...")
subprocess.run([python, "indicators/moving_averages.py"], check=True)

print("Step 3: Running strategy...")
subprocess.run([python, "strategies/strategy.py"], check=True)

print("\n✅ Gold Trading System completed successfully!")