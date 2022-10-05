#!/usr/bin/env python
import numpy as np
import datetime
import time
import pandas



gWorking = False


def main():
    debug('hello, this program is a timecard')
    timenow = datetime.datetime.now()
    run()
    time.sleep(3)
    run()



def run(working = gWorking):
    if working == True:
        clockOut()
    else:
        clockIn()




#*********************************888
def clockIn(tTime = datetime.datetime.now() ):
    debug('clocking In')
    debug(tTime)
    if gWorking ==True:
        err('double clock in detected')
    gWorking = True


def clockOut(tTime = datetime.datetime.now() ):
    debug('clocking Out')
    debug(tTime)
    if gWorking ==False:
        err('double clock out detected')
    gWorking = False


def debug(str =""):
    print(str, flush=True)
   

#*********************************888
def example():
    debug('hello, this program is an example')
    old_time = datetime.datetime.now()
    debug(old_time)
    new_time = old_time + datetime.timedelta(hours=2, minutes=10)
    debug(new_time)
    return new_time


#*********************************888
if __name__ == '__main__':
    main()
