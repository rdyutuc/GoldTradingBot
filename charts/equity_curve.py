import matplotlib.pyplot as plt

def plot_equity_curve(trades):

    balances = [10000]

    for trade in trades:
        balances.append(trade.balance)

    plt.figure(figsize=(10,5))

    plt.plot(balances)

    plt.title("Equity Curve")

    plt.xlabel("Trades")

    plt.ylabel("Balance ($)")

    plt.grid(True)

    plt.show()