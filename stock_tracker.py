# stock_tracker.py

import yfinance as yf
import json
from datetime import datetime

def estimate_fair_value(forward_eps, forward_pe_low, forward_pe_high):
    if forward_eps is None or forward_pe_low is None or forward_pe_high is None:
        return None
    forward_pe_mid = (forward_pe_low + forward_pe_high) / 2
    return forward_eps * forward_pe_mid

def determine_valuation_status(current_price, estimated_price):
    if estimated_price is None or current_price is None:
        return "Unknown"
    if current_price > estimated_price * 1.1:
        return "Overvalued"
    elif current_price < estimated_price * 0.9:
        return "Undervalued"
    else:
        return "Fair"

def fetch_stock_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        estimated_price = estimate_fair_value(
            info.get("forwardEps"),
            info.get("forwardPE", 0) * 0.8,
            info.get("forwardPE", 0) * 1.2
        )

        current_price = info.get("currentPrice")

        return {
            "symbol": ticker_symbol,
            "price": current_price,
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "eps": info.get("trailingEps"),
            "forward_eps": info.get("forwardEps"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "chg": info.get("regularMarketChange"),
            "chg_pct": info.get("regularMarketChangePercent"),
            "estimated_price": estimated_price,
            "valuation": determine_valuation_status(current_price, estimated_price)
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {ticker_symbol}: {e}")
        return {
            "symbol": ticker_symbol,
            "error": str(e)
        }

def main():
    with open("tracked_stocks.json", "r") as f:
        stock_list = json.load(f)

    results = []
    for symbol in stock_list:
        print(f"Fetching {symbol} ...")
        stock_data = fetch_stock_data(symbol)
        results.append(stock_data)

    output = {
        "last_updated": datetime.now().isoformat(),
        "stocks": results
    }

    with open("latest_data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("✅ Data saved to latest_data.json")

if __name__ == "__main__":
    main()
