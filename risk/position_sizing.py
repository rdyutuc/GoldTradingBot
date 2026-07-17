# Position Sizing Calculator

def calculate_position_size(account_balance,
                            risk_percent,
                            stop_loss_distance,
                            value_per_point=1):
    """
    Calculates position size based on account risk.

    account_balance : Account balance
    risk_percent : Percentage to risk (e.g. 1)
    stop_loss_distance : Distance from entry to stop loss
    value_per_point : Dollar value per point
    """

    risk_amount = account_balance * (risk_percent / 100)

    position_size = risk_amount / (stop_loss_distance * value_per_point)

    return position_size


# Example
account = 10000
risk = 1
stop_loss = 30

lot = calculate_position_size(account, risk, stop_loss)

print(f"Recommended Position Size: {lot:.2f}")