from stockfunctions import *



class Stock_Position:
    """
    Class that manages and trades a single stock
    """

    def __init__(self, ticker, value):
        self.ticker = ticker
        self.cash = value
        self.value = value
        self.amount = 0


    def __repr__(self):
        s = "Ticker: {}, Value: {}, Amount: {}".format(self.ticker,
            self.value, self.amount)

        return s


    def trading_algo(self, secs, rsi_per):
        """
        Trading algorithm based on Algo3
        """
        #The number of seconds after the beginning that the progrom should run
        print("Trading: {} for {} seconds".format(self.ticker, secs))

        t_end = time.time() + secs

        while (time.time() < t_end):

            RSI = RSI_short_term(self.ticker, rsi_per)
            p = get_live_price(self.ticker)
            b_amount = ((50 - RSI)//10)
            s_amount = ((RSI - 50)//10)

            if (b_amount == 0 and s_amount == 0):
                continue

            if RSI <= 50 and self.cash - (p * b_amount) >= 0:
                self.cash = self.cash - (p * b_amount)
                self.amount = self.amount + b_amount
                self.value = self.cash + (p * self.amount)

                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print('{}, BUY {}, {}, {}, {}, {}, {} shares'.format(
                    self.ticker,
                    b_amount,
                    p,
                    self.value,
                    current_time,
                    self.cash,
                    self.amount))
                continue

            elif RSI > 50 and self.amount> 0:
                if s_amount > self.amount:
                    self.cash = self.cash + (p * self.amount)
                    self.amount = 0
                    self.value = self.cash

                else:
                    self.cash = self.cash + (p * s_amount)
                    self.amount = self.amount - s_amount
                    self.value = self.cash + self.amount * p

                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                print('{}, SELL {}, {}, {}, {}, {}, {} shares'.format(
                    self.ticker,
                    s_amount,
                    p,
                    self.value,
                    current_time,
                    self.cash,
                    self.amount))
                continue

            else:
                continue

        #if self.amount> 0:
        #    p = get_live_price(self.ticker)
        #    self.cash = self.cash + self.amount * p
        #    print('SOLD {} shares at {}'.format(self.amount, p))
        #    self.amount = 0
        #    self.value = self.cash

        p = get_live_price(self.ticker)
        self.value = self.cash + (self.amount * p)

        return self.value, self.amount
