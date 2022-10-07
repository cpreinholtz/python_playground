#!/usr/bin/env python
import numpy as np
import datetime
import time
import pandas as pd



gWorking = False
gDf = False

#*********************************888

def init():

    readCsvFile()
    recalculateDiff()
    global gDf    

    debug(gDf.to_string())


def main():
    debug('hello, this program is a timecard')
    init()

    reportThisWeek()
    while True:
        run()

def run():
    global gWorking
    if gWorking == True:
        global gDf
        msg('you are working on' + gDf.at[len(gDf.index)-1, 'Proj'])
        input('press enter to clock OUT')
        clockOut()
    else:
        inp = input('Enter Project Name to clock IN:')
        clockIn(project = inp)
    debug(gDf.to_string())



def reportThisWeek(start_date = datetime.date.today(), end_date = datetime.date.today()+ datetime.timedelta(days = 1)):
    start_date = datetime.date.today()
    for x in range(6):
        start_date = datetime.date.today() - datetime.timedelta(days = x)
        end_date = start_date + datetime.timedelta(days = 1)
        msg('******************')
        report(start_date =start_date, end_date =  end_date)
    msg('******************')

#*********************************888
#%d/%m/%Y
def report(start_date = datetime.date.today(), end_date = datetime.date.today()+ datetime.timedelta(days = 1)):



    start_datetime = pd.to_datetime(start_date, format = "%Y-%m-%d")
    end_datetime = pd.to_datetime(end_date,  format = "%Y-%m-%d")

    msg('from ' + str(start_datetime) +' to ' + str(end_datetime) + ' you worked these hours:')
    global gDf

    inDatetimes = pd.to_datetime(gDf.loc[:,'In'], format = "%Y-%m-%d %H:%M:%S")
    outDatetimes = pd.to_datetime(gDf.loc[:,'Out'], format = "%Y-%m-%d %H:%M:%S")
    mask = ( inDatetimes > start_datetime) & (inDatetimes <= end_datetime)
    if any(mask):
        df2 = gDf.loc[mask]
        debug(df2)
        dff = df2.groupby(["Proj"]).Diff.sum().reset_index()
        msg(dff)
    else:
        msg('No work from ' + str(start_datetime) +' to ' + str(end_datetime))



def recalculateDiff():
    global gDf
    inDatetimes = pd.to_datetime(gDf.loc[:,'In'], format = "%Y-%m-%d %H:%M:%S")
    outDatetimes = pd.to_datetime(gDf.loc[:,'Out'], format = "%Y-%m-%d %H:%M:%S")
    gDf['Diff'] = outDatetimes - inDatetimes
    writeCsvFile()

#*********************************888
def createNew( data = [['Dev', None, None, None]] ):
    columns = ['Proj', 'In', 'Out', 'Diff']
    return pd.DataFrame(data, columns = columns)


def readCsvFile(fileName = './card.csv'):
    fileName = './card.csv'
    global gDf

    try:
        gDf = pd.read_csv(fileName, index_col=0)
    except:
        gDf = createNew()
        writeCsvFile()

    #if gDf.at[len(gDf.index)-1, 'Out'] == None or gDf.at[len(gDf.index)-1, 'Out'] == nan:
    if pd.isnull(gDf.at[len(gDf.index)-1, 'Out']) and pd.notnull(gDf.at[len(gDf.index)-1, 'In']):
        global gWorking
        gWorking = True
        debug('no clockout detected on last row')
        debug(gDf.at[len(gDf.index)-1, 'Out'])
    else:
        gWorking = False
        debug('clockout detected in last csv ')
        debug(gDf.at[len(gDf.index)-1, 'Out'])


def writeCsvFile(fileName = './card.csv'):
    global gDf
    gDf.to_csv(fileName)



#*********************************888
def clockIn(project ='NA' ):
    tTime = datetime.datetime.now()
    debug('clocking In')
    debug(tTime)
    global gWorking
    if gWorking ==True:
        err('double clock in detected')
        err(gWorking)
    gWorking = True
    addRow(project = project, inTime = tTime)
    writeCsvFile()

def addRow(project = 'NA' , inTime = datetime.datetime.now(), outTime = None,  diff = None):
    global gDf
    gDf = pd.concat( [gDf, createNew(data = [[project, inTime, outTime, diff]]) ], ignore_index=True)


#*********************************888
def clockOut( ):
    tTime = datetime.datetime.now()
    debug('clocking Out')
    debug(tTime)
    global gWorking
    if gWorking ==False:
        err('double clock out detected')
    gWorking = False
    updateLastOut(tTime)
    writeCsvFile()

def updateLastOut(outTime):
    global gDf
    debug(len(gDf.index))
    debug(gDf.at[0, 'Out'])
    inTime = pd.to_datetime(gDf.at[len(gDf.index)-1, 'In'] , format = "%Y-%m-%d %H:%M:%S")
    gDf.at[len(gDf.index)-1, 'Out'] = outTime
    gDf.at[len(gDf.index)-1, 'Diff'] = outTime - inTime




#*********************************888
def debug(str =""):
    print(str, flush=True)
def msg(str = ''):
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
