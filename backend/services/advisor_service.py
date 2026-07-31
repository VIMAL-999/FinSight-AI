def calculate_health(return_percentage):

    if return_percentage >= 20:
        return "Excellent"

    elif return_percentage >= 10:
        return "Good"

    elif return_percentage >= 0:
        return "Average"

    return "Poor"


def calculate_risk(num_holdings):

    if num_holdings >= 8:
        return "Low"

    elif num_holdings >= 4:
        return "Medium"

    return "High"


def diversification_score(num_holdings):

    score = min(num_holdings * 15, 100)

    return score


def recommendation(return_percentage):

    if return_percentage >= 20:
        return "Portfolio performing strongly. Continue holding."

    elif return_percentage >= 10:
        return "Healthy growth. Monitor positions regularly."

    elif return_percentage >= 0:
        return "Moderate returns. Consider adding diversification."

    return "Portfolio is underperforming. Review your holdings."