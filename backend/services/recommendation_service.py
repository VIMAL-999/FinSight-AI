def generate_recommendation(
    buy_price,
    current_price,
    quantity
):

    profit_percent = (
        (current_price - buy_price)
        / buy_price
    ) * 100

    reasons = []

    score = 50

    if profit_percent > 20:
        score += 30
        reasons.append(
            "Current profit exceeds 20%"
        )

    elif profit_percent > 10:
        score += 20
        reasons.append(
            "Healthy positive return"
        )

    elif profit_percent >= 0:
        score += 10
        reasons.append(
            "Investment remains profitable"
        )

    else:
        score -= 20
        reasons.append(
            "Investment is currently at a loss"
        )

    if quantity >= 20:
        reasons.append(
            "Large holding size"
        )

    else:
        reasons.append(
            "Position size is healthy"
        )

    if score >= 80:

        recommendation = "BUY"

        risk = "Low"

    elif score >= 60:

        recommendation = "HOLD"

        risk = "Medium"

    else:

        recommendation = "SELL"

        risk = "High"

    return {
        "recommendation": recommendation,
        "confidence": min(score, 100),
        "risk": risk,
        "reason": reasons
    }