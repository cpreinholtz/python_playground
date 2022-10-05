#!/usr/bin/env python
import numpy as np
import datetime
import time
import pandas as pd



gWorking = False
gDf = False

#*********************************888
def main():
    debug('hello, this program is a timecard')
    createNew()
    global gDf
    debug(gDf)


    runTwo()
    runTwo()

def runTwo():
    run()
    debug(gDf)
    run()
    debug(gDf)

def run():
    global gWorking
    if gWorking == True:
        input('press enter to clock OUT')
        clockOut()
    else:
        inp = input('Enter Project Name to clock IN:')
        clockIn(project = inp)




#*********************************888
#project, in time, out time
def createNew( data = [['Dev', datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(hours = 1)]] ):
    columns = ['Proj', 'In', 'Out']
    global gDf
    gDf = pd.DataFrame(data, columns = columns)




#*********************************888
def clockIn(tTime = datetime.datetime.now(), project ='NA' ):
    debug('clocking In')
    debug(tTime)
    global gWorking
    if gWorking ==True:
        err('double clock in detected')
        err(gWorking)
    gWorking = True
    addRow(project, tTime, tTime)

def addRow(project = 'NA' , inTime = datetime.datetime.now(), outTime = None):
    global gDf
    gDf = pd.concat( [gDf, pd.DataFrame([project, inTime, outTime]) ])


#*********************************888
def clockOut(tTime = datetime.datetime.now() ):
    debug('clocking Out')
    debug(tTime)
    global gWorking
    if gWorking ==False:
        err('double clock out detected')
    gWorking = False
    #updateLastOut()

def updateLastOut(outTime = datetime.datetime.now()):
    global gDf
    gDf.loc[len(gDf.index)][Out] = outTime



#*********************************888
def debug(str =""):
    print(str, flush=True)

def err(str =""):
    print("**ERROR DETECTED*******************", flush=True)
    print(str, flush=True)
    print("***********************************", flush=True)

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
