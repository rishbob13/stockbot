from Stock_Position import *
from multiprocessing import Process, Pool
from threading import Thread



class Portfolio:
    """
    Class that manages multiple instances of the Stock_Positions object at once
    """

    def __init__(self, tickers, netl, RS):
        num = len(tickers)
        if RS == True:
            self.positions = [RS_Position(t, netl//num) for t in tickers]
        else:
            self.positions = [Stock_Position(t, netl//num) for t in tickers]
        self.netl = netl
        self.RS = RS


    def __repr__(self):
        s = ""
        self.netl_ref()

        for t in self.positions:
            s = s + str(t) + "\n"

        s = s + "Net Worth: {}".format(self.netl)
        return s


    def netl_ref(self):
        self.netl = np.sum([t.value for t in self.positions])

        return self.netl


    def check_positions(self):
        return print(str(self))


    def simul_run(self, secs, RSI_per):
        threads = []

        for i in range(len(self.positions)):
            process = Thread(
                target = Stock_Position.trading_algo,
                args = [self.positions[i], secs, RSI_per],
                daemon = True)
            process.start()
            threads.append(process)

        for p in threads:
            p.join()

        #if self.RS == True:
        #    for t in self.positions:
        #        t.close_position()

        return self.check_positions()
