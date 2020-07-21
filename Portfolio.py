from Stock_Position import *
from multiprocessing import Process, Pool
from threading import Thread


class Portfolio:
    """
    Class that manages multiple instances of the Stock_Positions object at once
    """


    def __init__(self, tickers, netl):
        num = len(tickers)
        self.tickers = [Stock_Position(t, netl//num) for t in tickers]
        self.netl = netl


    def __repr__(self):
        s = ""
        self.netl_ref()

        for t in self.tickers:
            s = s + str(t) + "\n"

        s = s + "Net Worth: {}".format(self.netl)
        return s


    def netl_ref(self):
        self.netl = np.sum([t.value for t in self.tickers])

        return self.netl


    def check_positions(self):
        return print(str(self))


    def simul_run(self):
        threads = []

        for i in range(len(self.tickers)):
            process = Thread(
                target = Stock_Position.trading_algo,
                args = [self.tickers[i], 3600, 60],
                daemon = True)
            process.start()
            threads.append(process)

        for p in threads:
            p.join()

        return self.check_positions()
