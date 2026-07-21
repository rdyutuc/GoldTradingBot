def print_report(results):

    print("=" * 40)
    print("BACKTEST REPORT")
    print("=" * 40)

    for key, value in results.items():

        if key in (
            "Starting Balance",
            "Ending Balance",
            "Net Profit",
            "Average Win",
            "Average Loss",
            "Largest Win",
            "Largest Loss",
        ):
            print(f"{key:<20}: ${value:,.2f}")

        elif key == "Win Rate":
            print(f"{key:<20}: {value:.2f}%")

        elif key == "Profit Factor":

            if value == float("inf"):
                print(f"{key:<20}: Infinity")
            else:
                print(f"{key:<20}: {value:.2f}")

        elif key == "Maximum Drawdown":
            print(f"{key:<20}: {value:.2f}%")

        else:
            print(f"{key:<20}: {value}")