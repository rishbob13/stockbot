import yahoo_fin
from yahoo_fin.stock_info import *
import yfinance as yf

import time

import numpy as np



def RSI_short_term(ticker, secs):
    """
    RSI calculator for short term (intraday) momentum
    """
    arr, gain, loss = [], [], []
    prev = 0
    t_end = time.time() + (secs + 1)

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

    rs = (np.sum(gain)/len(arr))/(np.sum(loss)/len(arr))
    rsi = 100 - 100/(1 + rs)

    return rs, rsi, arr[0], arr[len(arr) - 1], len(arr), gain, loss



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
