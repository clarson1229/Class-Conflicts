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


class ClassStruct(object):
    def __init__(self, name: str='', days: list = [], startT: str='', endT: str=''):
        self.name = name
        self.days = days
        self.startT = startT
        self.endT = endT


def open_file(fileName: str) -> dict:
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


        file.close()
    except IOError:
        print("File not found Enter a new file")


def main():
    open_file('classes.csv')

main()