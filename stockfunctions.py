import yahoo_fin
from yahoo_fin.stock_info import *
import yfinance as yf

import time

import numpy as np

"""
Functions useful for evaluating stock momentum to be used in the bots
"""



def RSI_short_term(ticker, secs):
    """
    RSI calculator for short term (intraday) momentum
    """
    arr, gain, loss = [], [], []
    prev = 0
    t_end = time.time() + secs

    while (time.time() < t_end):
        p = get_live_price(ticker)
        arr.append(p)
        if len(arr) > 1:
            if p > prev:
                gain.append(p - prev)
            elif p < prev:
                loss.append(prev - p)
        prev = p
        time.sleep(0.8)

    rs = (np.sum(gain)/len(arr))**2.5/(np.sum(loss)/len(arr))**2.5
    #seems to be well calibrated for periods of 60 secs, all over the place
    #for smaller periods like 14
    rsi = 100 - 100/(1 + rs)

    #return rs, rsi, arr[0], arr[len(arr) - 1], len(arr), gain, loss
    return rsi


def RSI_short_term_tracker(ticker, tim, RSI_per):
    """
    Test of RSI_short_term acuracy and stock momentum tracking ability
    """
    count = 1
    t_end = time.time() + tim

    while time.time() < t_end:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("{}, {}, {}, {}".format(current_time, count,
            RSI_short_term(ticker, RSI_per), get_live_price(ticker)))
        count += 1


def RSI_long_term(ticker, days):
    """
    RSI calculator for long term (3 days or longer) momentum
    """
    p = get_live_price(ticker)
    arr, gain, loss = [], [], []
    prev = 0
    tick = yf.Ticker(ticker)
    hist = tick.history(period = "{}d".format(days + 1))
    closes = hist['Close']

    for i in range(len(closes[:-1])):
        if closes[i + 1] > closes[i]:
            gain.append(closes[i + 1] - closes[i])
        elif closes[i + 1] < closes[i]:
            loss.append(closes[i] - closes[i + 1])

    rs = (np.sum(gain)/days)/(np.sum(loss)/days)
    rsi = 100 - 100/(1 + rs)

    return rsi



def EMA_short_term(ticker, secs):
    """
    RSI calculator for short term (intraday)
    """
    arr = []
    t_end = time.time() + (secs + 1)

    while (time.time() < t_end):
        p = get_live_price(ticker)
        arr.append(p)
        time.sleep(1)

    V = get_live_price(ticker)
    s = 2
    d = secs
    m = (s/(1 + d))

    EMAo = np.mean(arr)
    EMAn = (V * m) + EMAo * (1 - m)

    return EMAn



def EMA_long_term(ticker, days):
    """
    EMA calculator for long term (3 days or more)
    """
    tick = yf.Ticker(ticker)
    hist = tick.history(period = "{}d".format(days - 1))
    closes = hist['Close']

    V = get_live_price(ticker)
    s = 2
    d = days
    m = (s/(1 + d))

    EMAy = np.mean(closes)
    EMAt = (V * m) + EMAy * (1 - m)

    return EMAt
