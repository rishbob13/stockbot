from Portfolio import *
import robin_stocks as rs

login = rs.login("rishabhv@hotmail.com", "Sandbox0!23")

t = ["JETS", "IVZ"]
p1 = Portfolio(t, 200, False)

#p1.simul_run(3600, 60)
