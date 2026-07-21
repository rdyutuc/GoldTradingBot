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
        "Starting Balance": start_balance,
        "Ending Balance": end_balance,
        "Net Profit": end_balance - start_balance,
        "Total Trades": total,
        "Wins": wins,
        "Losses": losses,
        "Win Rate": win_rate,
        "Profit Factor": profit_factor,
        "Average Win": average_win,
        "Average Loss": average_loss,
        "Largest Win": largest_win,
        "Largest Loss": largest_loss,
    }