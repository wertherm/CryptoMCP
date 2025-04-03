import ccxt
import pandas as pd
import pandas_ta as ta
import numpy as np

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

def get_crypto(exchange_id, symbol, timeframe='1h', limit=20):
    exchange = getattr(ccxt, exchange_id)()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    # Convert to DataFrame for pandas_ta
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df['close'].values

@mcp.tool()
def analyze_bollinger(close_prices, period=20, deviation=2):
    """Analisa se uma criptomoeda está no topo ou fundo das bandas de bollinger

    Args:
        close_prices (): Preço de fechamento
    
    Returns:
        string: Resultado da análise em string (top = topo, bottom = fundo, neutral = neutro)
    """
    # Convert numpy array to pandas Series for pandas_ta
    series = pd.Series(close_prices)
    bbands = ta.bbands(series, length=period, std=deviation)
    
    last_price = close_prices[-1]
    if last_price >= bbands['BBU_' + str(period) + '_' + str(float(deviation)) + '.0'].iloc[-1]:
        return "top"
    elif last_price <= bbands['BBL_' + str(period) + '_' + str(float(deviation)) + '.0'].iloc[-1]:
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