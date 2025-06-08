import numpy as np
import datetime, threading, time
import Scope

def ticktock():
    twopi = 2 * np.pi
    tick = twopi / 1000
    while True:
        for i in range(0,1000):
            print("   %f" % ((1.0 + np.sin(float(i) * tick))/2.0))
            time.sleep(0.010)

#timerThread = threading.Thread(target=ticktock)
#timerThread.daemon = True
#timerThread.start()

s = Scope.Scope(buffsize=10,initval=0,max=100,min=0)

while True:
    for i in range(0,100):
        s.value = float(i) + 0.1
        s.debug()
        time.sleep(1)

twopi = 2 * np.pi
tick = twopi / 10
icount = 0
val = []
while True:
    for i in range(0,10):
        thisv = (1.0 + np.sin(float(i) * tick))/2.0
        val.append(thisv)
        if icount >= 10:
            val.pop(0)
        print("[%d] : %f" % (icount,thisv))
        print(val)
        icount = icount + 1
        time.sleep(0.5)

