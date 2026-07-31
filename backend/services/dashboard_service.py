def investment_score(return_percentage, num_holdings):

    score = 50

    if return_percentage > 0:
        score += min(int(return_percentage), 30)

    score += min(num_holdings * 5, 20)

    return min(score, 100)


def diversification_warning(allocation):

    if len(allocation) == 0:
        return "Portfolio is empty."

    highest = max(allocation.values())

    if highest > 40:
        return "High concentration risk. Consider diversifying."

    return "Portfolio is well diversified."