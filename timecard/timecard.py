#!/usr/bin/env python

import datetime
import time
import pandas as pd


import PySimpleGUI as sg



gWorking = False
gDf = False
gWindow = False

#*********************************
#
#*********************************

#read csv, calculate diffs
def init():
    readCsvFile()
    recalculateDiff()



#def initGui():
    global gWorking 
    global gWindow

    layout = [
        [sg.Text("", key= 'prompt')], 
        [sg.Input(gDf.at[len(gDf.index)-1, 'Proj'], key='project', disabled=gWorking)],
        [sg.Button("CLK IN",key= "CLK IN", disabled=gWorking)], 
        [sg.Text('Time elapsed: ', key='time')], 
        [sg.Button("CLK OUT",key="CLK OUT", disabled=not gWorking)],
        [sg.Button("Refresh")],
        [sg.Text("", font = ("Courier", 11), key= 'report')], 
    ]    
    gWindow = sg.Window("Demo", layout, finalize=True)

    updateGui()


def updateGui():
    gWindow['CLK IN'].update(disabled=gWorking)
    gWindow['project'].update(disabled=gWorking)
    gWindow['CLK OUT'].update(disabled=not gWorking)

    if( gWorking):
        gWindow['prompt'].update('Currently Working On')                         #top prompt
        gWindow['project'].update(gDf.at[len(gDf.index)-1, 'Proj'] )            #current project name
        gWindow['time'].update('Time elapsed: ' + 
            str(getLastDiff(datetime.datetime.now())) )         #current working time
    else:
        gWindow['prompt'].update('Enter Project Name Then Clock IN')
        gWindow['time'].update('Time elapsed: ')         #
    gWindow['report'].update(reportThisWeek())





#init, report, run
def main():
    debug('hello, this program is a timecard')
    init()


    global gWindow
    while True:
        event, values = gWindow.read()
        if event == "CLK IN":
            clockIn(values['project'])
        elif event == "CLK OUT":
            clockOut()
        elif event == sg.WIN_CLOSED:
            #reportThisWeek()
            break
        elif event == "Refresh":
            debug("handled in update gui")
        updateGui()





#*********************************
# Actions
#*********************************
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


#*********************************
# Reports
#*********************************

def reportThisWeek(start_date = datetime.date.today(), end_date = datetime.date.today()+ datetime.timedelta(days = 1)):
    start_date = datetime.date.today()
    returnme = "WEEKLY REPORT:\n"
    for x in range(6):
        start_date = datetime.date.today() - datetime.timedelta(days = x)
        end_date = start_date + datetime.timedelta(days = 1)
        msg('******************')
        dailyResult  = report(start_date =start_date, end_date =  end_date)

        if dailyResult[0]:
            returnme =  returnme+"\n"+ start_date.strftime("%D") + "\n" + dailyResult[1].to_markdown(index=False) + "\n"
    msg('******************')
    return returnme


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
        #debug(df2)
        dff = df2.groupby(["Proj"]).Diff.sum().reset_index()
        msg(dff)
        return [True, dff]
    else:
        msg('No work from ' + str(start_datetime) +' to ' + str(end_datetime))
        return [False]




#*********************************
#Calculating time worked
#*********************************

def recalculateDiff():#recalculte all
    global gDf
    inDatetimes = pd.to_datetime(gDf.loc[:,'In'], format = "%Y-%m-%d %H:%M:%S")
    outDatetimes = pd.to_datetime(gDf.loc[:,'Out'], format = "%Y-%m-%d %H:%M:%S")
    gDf['Diff'] = outDatetimes - inDatetimes
    writeCsvFile()



#*********************************
#Data Frame
#*********************************
#create a completely new dataframe and return it
def createNew( data = [['Dev', None, None, None]] ):
    columns = ['Proj', 'In', 'Out', 'Diff']
    return pd.DataFrame(data, columns = columns)


#add row to dataframe using passed inTime= NOW
def addRow(project = 'NA' , inTime = datetime.datetime.now(), outTime = None,  diff = None):
    global gDf
    gDf = pd.concat( [gDf, createNew(data = [[project, inTime, outTime, diff]]) ], ignore_index=True)




#Add out and diff to current data frame using passed in outTime
def updateLastOut(outTime):
    global gDf
    #debug(len(gDf.index))
    #debug(gDf.at[0, 'Out'])

    gDf.at[len(gDf.index)-1, 'Out'] = outTime
    gDf.at[len(gDf.index)-1, 'Diff'] = getLastDiff(outTime)

def getLastDiff(outTime):
    global gDf
    inTime = pd.to_datetime(gDf.at[len(gDf.index)-1, 'In'] , format = "%Y-%m-%d %H:%M:%S")
    return (outTime - inTime)

    


#*********************************
#CSV Manipulation
#*********************************
def readCsvFile(fileName = './card.csv'):
    fileName = './card.csv'
    global gDf

    #try reading file, else create a new one
    try:
        gDf = pd.read_csv(fileName, index_col=0)
    except:
        gDf = createNew()
        writeCsvFile()

    #set state variable gWorking based on last in and out times
    if pd.isnull(gDf.at[len(gDf.index)-1, 'Out']) and pd.notnull(gDf.at[len(gDf.index)-1, 'In']):
        global gWorking
        gWorking = True
        debug('no clockout detected on last row')
        debug(gDf.at[len(gDf.index)-1, 'Out'])
    else:
        gWorking = False
        debug('clockout detected in last csv ')
        debug(gDf.at[len(gDf.index)-1, 'Out'])

#dump dataframe to CSV, overwrites existing data completly
def writeCsvFile(fileName = './card.csv'):
    global gDf
    gDf.to_csv(fileName)





#*********************************
#Printing and debugging
#*********************************
def debug(str =""):
    print(str, flush=True)
def msg(str = ''):
    print(str, flush=True)
def err(str =""):
    print("**ERROR DETECTED*******************", flush=True)
    print(str, flush=True)
    print("***********************************", flush=True)

#show how time delta function works
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
