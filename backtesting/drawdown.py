def maximum_drawdown(trades, starting_balance=10000):
    """
    Calculates the maximum percentage drawdown from the trade history.
    """

    peak = starting_balance
    max_drawdown = 0

    for trade in trades:

        if trade.balance > peak:
            peak = trade.balance

        drawdown = (peak - trade.balance) / peak * 100

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return round(max_drawdown, 2)