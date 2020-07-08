from stockfunctions import *



def stockbot1(ticker, secs, rsi_per, RSI_level):
    """
    Prototype bot

    @ticker is the ticker of the stock that the bot will trade
    @secs is the number of seconds the bot will run
    @rsi_per is the period value that the RSI calculator will use
    @RSI_level is the rsi value that the bot will use to decide on how it will
        trade
    """
    #The net liquid value of all assets
    netl = 2000
    #Cash on hand after buying stock
    cash = 2000
    #amount of stock held
    amount = 0
    #Price that the single stock is bought at
    buy_p = 0
    #The number of seconds after the beginning that the progrom should run
    t_end = time.time() + (secs + 1)

    while (time.time() < t_end):
        while amount == 0:
            if RSI_short_term(ticker, rsi_per) < RSI_level:
                p = get_live_price(ticker)
                buy_p = p
                cash = cash - p
                amount += 1
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print('BUY, {}, {}, {}, {}'.format(p, netl, current_time, cash))

        while amount > 0:
            if RSI_short_term(ticker, rsi_per) > (100 - RSI_level):
                p = get_live_price(ticker)
                cash = cash + p
                netl = netl + (p - buy_p)
                amount -= 1
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print('SELL, {}, {}, {}, {}'.format(p, netl, current_time, cash))

    return netl
