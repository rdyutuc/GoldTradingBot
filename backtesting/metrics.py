def win_rate(wins, losses):

    total = wins + losses

    if total == 0:
        return 0

    return wins / total * 100


def net_profit(start_balance, end_balance):

    return end_balance - start_balance