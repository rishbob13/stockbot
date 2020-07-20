from stockfunctions import *



def stockbot2(ticker, secs, rsi_per):
    """
    Second prototype bot that can hold more than 1 share of a stock

    @ticker is the ticker of the stock that the bot will trade
    @secs is the number of seconds the bot will run
    @rsi_per is the period value that the RSI calculator will use
    """
    #The net liquid value of all assets
    netl = 2000
    #Cash on hand after buying stock
    cash = 2000
    #amount of stock held
    amount = 0
    #The number of seconds after the beginning that the progrom should run
    t_end = time.time() + secs

    while (time.time() < t_end):

        RSI = RSI_short_term(ticker, rsi_per)
        p = get_live_price(ticker)

        if RSI < 33 and cash - p >= 0:
            cash = cash - p
            amount += 1
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('BUY, {}, {}, {}, {}, {} shares'.format(p, netl,
                current_time, cash, amount))
            continue

        elif RSI < 67 and amount > 0:
            cash = cash + p
            amount -= 1
            netl = cash + amount * p
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('SELL, {}, {}, {}, {}, {} shares'.format(p, netl,
                current_time, cash, amount))
            continue

        else:
            continue

    if amount > 0:
        p = get_live_price(ticker)
        cash = cash + amount * p
        print('SOLD {} shares at {}'.format(amount, p))
        amount = 0
        netl = cash


    return netl
