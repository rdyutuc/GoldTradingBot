def calculate_performance(trades, start_balance, end_balance):

    
    gross_profit = 0
    gross_loss = 0

    wins = 0
    losses = 0

    largest_win = 0
    largest_loss = 0

    win_amounts = []
    loss_amounts = []

    for trade in trades:

        if trade.result == "WIN":
            wins += 1
            gross_profit += trade.profit

            win_amounts.append(trade.profit)

            if trade.profit > largest_win:
                largest_win = trade.profit

        else:
            losses += 1
            gross_loss += abs(trade.profit)

            loss_amounts.append(abs(trade.profit))

            if abs(trade.profit) > largest_loss:
                largest_loss = abs(trade.profit)

    total = wins + losses

    win_rate = (wins / total * 100) if total else 0

    if gross_loss == 0:
        profit_factor = float("inf")
    else:
        profit_factor = gross_profit / gross_loss

    average_win = (
        sum(win_amounts) / len(win_amounts)
        if win_amounts
        else 0
    )

    average_loss = (
        sum(loss_amounts) / len(loss_amounts)
        if loss_amounts
        else 0
    )        

    return {
        "Starting Balance": f"${start_balance:,.2f}",
        "Ending Balance": f"${end_balance:,.2f}",
        "Net Profit": f"${end_balance-start_balance:,.2f}\n",
        "Total Trades": total,
        "Wins": wins,
        "Losses": losses,
        "Win Rate": f"{win_rate:.2f}%\n",
        "Profit Factor": (
            "Infinity\n"
            if profit_factor == float("inf")
            else f"{profit_factor:.2f}\n"
        ),
        "Average Win": f"${average_win:,.2f}",
        "Average Loss": f"${average_loss:,.2f}\n",
        "Largest Win": f"${largest_win:,.2f}",
        "Largest Loss": f"${largest_loss:,.2f}\n",
    }