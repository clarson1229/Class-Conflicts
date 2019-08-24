# Author :  Connor Larson
# Goal: get list of people who are free at certain times.

# notes
# datetime.time(hours,minutes)
#
#
import datetime
from enum import Enum
import os
import csv

class Days(Enum):
    M = 1
    T = 2
    W = 3
    TU = 4
    F = 5

class Student(object):
    def __init__(self, name: str='', classList: list=[]):
        self.name = name
        self.classList = classList


class ClassStruct(object):
    def __init__(self, startT , endT, name: str='', days: list = []):
        self.name = name
        self.days = days
        self.startT = startT
        self.endT = endT


def open_file(fileName: str, studentList: dict) -> dict:
    """ Opens CSV file and reads   """
    try:
        # opens file and uses CSV reader to get each line into a list then iterates through and stores into a dictionary
        file = open(fileName, mode="r")
        fileCSV = csv.reader(file)
        data ={}
        for line in fileCSV:
            tempName = line[0]
            className = line[1]
            days = line[2].split('-')
            tempStartTime = line[3].split(' ')

            sHour, sMin = tempStartTime[0].split(':')
            sHour = int(sHour)
            sMin = int(sMin)
            if tempStartTime[1] == 'PM' and sHour != 12:
                sHour += 12
            # print('Start: ' + str(sHour) + ':' + str(sMin))
            tempEndTime = line[4].split(' ')
            eHour, eMin = tempEndTime[0].split(':')
            eHour = int(eHour)
            eMin = int(eMin)
            if tempEndTime[1] == 'PM' and eHour != 12:
                eHour += 12
            # print('End:' + str(eHour) + ':' + str(eMin))
            tStart = datetime.time(sHour, sMin)
            tEnd = datetime.time(eHour,eMin)

            tempClass = ClassStruct(tStart, tEnd, className, days)

            if tempName in studentList.keys() :
                studentList[tempName].append(tempClass)
            else:
                studentList[tempName] = [tempClass]

        file.close()
        return studentList
    except IOError:
        print("File not found Enter a new file")

def find_available(studentList, day, startT, endT ):
    for student in studentList:
        available = True
        for className in studentList[student]:
            if day in className.days:
                if max(startT, className.startT) < min(endT, className.endT):
                    available = False
                    print(student, 'has a Conflict with class ', className.name, 'at ', className.startT, className.endT , ' with interval', startT, endT,)
        if available:
            print(student, 'is available')
#                 no classes on that day and therefore available

def getData(prompt, targetData, warning)-> str:
    """Given the prompt and target Data function will run until given data is in target data range"""
    data = ''
    while True:
        data = input(prompt).upper().strip()
        # if the user just presses enter it catches it
        if data == '':
            print(warning)
        # if the given input is one of the accepted values
        elif data in targetData:
            return data
        else:
            print(warning)

def getTime(prompt, warning)-> str:
    data =''
    while True:
        data = input(prompt).upper().strip()
        # if the user just presses enter it catches it
        if data == '':
            print(warning)
        # if the given input is one of the accepted values
        elif ':' in data :
            if ' ' in data:
                if 'AM' or 'PM' in data:
                    print('true')
                    return data

        else:
            print(warning)

def formatTime(time)-> datetime:
    tempTime = time.split(' ')
    hour, min = tempTime[0].split(':')
    hour = int(hour)
    min = int(min)

    if tempTime[1] == 'PM' and hour != 12:
        hour += 12
    returnTime = datetime.time(hour, min)
    return returnTime


def main():
    studentList = {}
    studentList = open_file('classes.csv', studentList)
    # for student in studentList:
    #     for className in studentList[student]:
    #         print(className.name, className.days, className.startT, className.endT)

    running = 1
    while running == 1:
        # info for the running or not function
        runPrompt = """      Class Viewer \n
        1. Open Check Conflicts
        Q. Quit
    >>"""
        runWarning = "Input Must be 1 or Q"
        runTarget = "1,Q"
        program = getData(runPrompt, runTarget, runWarning)
        if program == "1":
            # getting input variables
            # Day
            dayPrompt = """      Enter the Day You want to check M-T-W-R-F
    >>"""
            dayWarning = "Input Must be one of the following: M-T-W-R-F"
            dayTarget = "M,T,W,R,F"
            dayToCheck = getData(dayPrompt, dayTarget, dayWarning)
            # start time
            timePrompt = """      Time Range Start? (##:## AM/PM)
    >> """
            timeWarning = "Input Must be in the format (12:00 PM) the time separated by :, space, AM or PM "
            intervalStart = getTime(timePrompt, timeWarning)
            # end time
            timePrompt = """      Time Range End? (##:## AM/PM)
    >> """
            timeWarning = "Input Must be in the format (12:00 PM) the time separated by :, space, AM or PM "
            intervalEnd = getTime(timePrompt, timeWarning)

            testStart = formatTime(intervalStart)
            testEnd   = formatTime(intervalEnd)
            find_available(studentList, dayToCheck, testStart, testEnd)

        else:
            break




main()