import ccxt
import talib
import numpy as np

def get_crypto(exchange_id, symbol, timeframe='1h', limit=20):
    exchange = getattr(ccxt, exchange_id)()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    close_prices = np.array([candle[4] for candle in ohlcv], dtype=np.float64)
    return close_prices

def analyze_bollinger(close_prices, period=20, deviation=2):
    upper, middle, lower = talib.BBANDS(close_prices, timeperiod=period, nbdevup=deviation, nbdevdn=deviation, matype=0)
    last_price = close_prices[-1]
    if last_price >= upper[-1]:
        return "top"
    elif last_price <= lower[-1]:
        return "bottom"
    return "neutral"

def buy(exchange_id, symbol, amount):
    exchange = getattr(ccxt, exchange_id)()
    order = exchange.create_market_buy_order(symbol, amount)
    return order

def mcp_decision(exchange_id, symbol, amount):
    prices = get_crypto(exchange_id, symbol)
    position = analyze_bollinger(prices)
    if position == "bottom":
        order = buy(exchange_id, symbol, amount)
        return f"Buying {amount} of {symbol} - Order: {order}"
    return "No buy signal."

# Exemplo de uso
exchange_id = "binance"
symbol = "BTC/USDT"
amount = 0.001
print(mcp_decision(exchange_id, symbol, amount))