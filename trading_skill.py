import ccxt

def execute_trade(symbol, action, amount):
    """
    这是一个被 AstrBot 调用的函数
    """
    # 这里的配置保存在你本地，不发给飞书
    exchange = ccxt.hyperliquid({
        'apiKey': '0xC632aFEd7fA0145E8c0d146B3099A8A51A7EFBB2',
        'secret': '0x2e707cdebac3dcda26e20fda414433d29aae394afba7b5957dd00fa8449907c0', # 建议用测试钱包
    })
    
    if action == "buy":
        return exchange.create_market_buy_order(symbol, amount)
    elif action == "sell":
        return exchange.create_market_sell_order(symbol, amount)