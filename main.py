import MetaTrader5 as mt5

# Connect to MT5
if not mt5.initialize():
    print("Connection failed!")
    print(mt5.last_error())
    quit()

print("Connected to MetaTrader 5!")

# Display account information
account = mt5.account_info()

if account:
    print(f"Login: {account.login}")
    print(f"Balance: ${account.balance}")
    print(f"Equity: ${account.equity}")
    print(f"Server: {account.server}")

mt5.shutdown()
