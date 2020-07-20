from stockfunctions import *



def stockbot3(ticker, secs, rsi_per):
    """
    third prototype able to buy in bulk

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
        b_amount = ((50 - RSI)//10)
        s_amount = ((RSI - 50)//10)

        if RSI <= 50 and cash - (p * b_amount) >= 0:
            cash = cash - (p * b_amount)
            amount = amount + b_amount
            netl = cash + (p * amount)

            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('BUY {}, {}, {}, {}, {}, {} shares'.format(b_amount, p, netl,
                current_time, cash, amount))
            continue

        elif RSI > 50 and amount > 0:
            if s_amount > amount:
                cash = cash + (p * amount)
                amount = 0
                netl = cash

            else:
                cash = cash + (p * s_amount)
                amount = amount - s_amount
                netl = cash + amount * p

            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('SELL {}, {}, {}, {}, {}, {} shares'.format(s_amount, p, netl,
                current_time, cash, amount))
            continue

        else:
            continue

    #if amount > 0:
    #    p = get_live_price(ticker)
    #    cash = cash + amount * p
    #    print('SOLD {} shares at {}'.format(amount, p))
    #    amount = 0
    #    netl = cash

    p = get_live_price(ticker)
    netl = cash + amount * p


    return netl, amount
