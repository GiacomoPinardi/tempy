#!/usr/bin/python

from time import sleep
from os import listdir
from os.path import exists
import numpy

# refresh time
global delay
delay = 1

global mainFolder
mainFolder = "/sys/bus/platform/devices/coretemp.0/hwmon/hwmon0/"

global data

# color
BLACK = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'

def printHello () :
    print "*****               TemPy             *****"
    print "/                                         /"
    print "/                    by                   /"
    print "/                                         /"
    print "/             Giacomo Pinardi             /"
    print "/                                         /"
    print "/                  (2015)                 /"
    print "/                                         /"
    print "*** www.github.com/GiacomoPinardi/tempy ***\n"

def readCoresInformation ():
    maxCore = 0
    all_files = listdir(mainFolder)
    for f in all_files:
        if (f.find('input') != -1):
            number = f.split('_')[0][4:]
            if (maxCore < number):
                maxCore = number

    # generating 2D array with numpy
    global data
    data = numpy.empty((int(maxCore), 2), dtype='object')

    for i in range(int(maxCore)):
        data[i][0] = readLabel(i+1)
        data[i][1] = readValues(i+1)

def printCoreInformation () :
    global data

    # clear cli
    print "\033c"

    printHello()

    for d in data:
        toPrint = d[0] + ": \t\t"
        if (int(d[1])) >= 70:
            toPrint += RED
        elif (int(d[1]) >= 40):
            toPrint += YELLOW
        else:
            toPrint += GREEN

        toPrint += d[1] + BLACK + unichr(0260) + "C"
        print toPrint

    print "\n[Ctrl+Z to stop]"

def readValues (coreNumber) :
    file = open(mainFolder + 'temp' + str(coreNumber) + '_input', 'r')
    return file.read()[::-1][4:][::-1]

def readLabel (coreNumber) :
    file = open(mainFolder + 'temp' + str(coreNumber) + '_label', 'r')
    return file.read()[::-1][1:][::-1]

def loop():
    if exists(mainFolder):
        while True:
            readCoresInformation()
            printCoreInformation()
            sleep(delay)
    else:
        print "Cannot find " + mainFolder + "\nAre you on Linux?"


# Main:
loop()
#
