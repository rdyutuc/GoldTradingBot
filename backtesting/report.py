def print_report(results):

    print("=" * 40)

    print("BACKTEST REPORT")

    print("=" * 40)

    for key, value in results.items():

        print(f"{key:<20}: {value}")