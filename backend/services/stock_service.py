import yfinance as yf


def get_stock_price(symbol: str):

    ticker = yf.Ticker(symbol)

    info = ticker.info

    return {
        "symbol": symbol.upper(),
        "company": info.get("longName"),
        "current_price": info.get("currentPrice"),
        "currency": info.get("currency"),
        "sector": info.get("sector"),
        "industry": info.get("industry")
    }


def get_live_price(symbol: str):

    ticker = yf.Ticker(symbol)

    info = ticker.info

    return info.get("currentPrice")