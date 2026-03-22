import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

def execute_trade(symbol, action, amount):
    """
    这是一个被 AstrBot 调用的函数
    """
    api_key = os.getenv("HYPERLIQUID_API_KEY", "")
    secret = os.getenv("HYPERLIQUID_SECRET", "")
    if not api_key or not secret:
        raise ValueError("Missing HYPERLIQUID_API_KEY or HYPERLIQUID_SECRET")
    exchange = ccxt.hyperliquid({
        'apiKey': api_key,
        'secret': secret,
    })
    
    if action == "buy":
        return exchange.create_market_buy_order(symbol, amount)
    elif action == "sell":
        return exchange.create_market_sell_order(symbol, amount)
