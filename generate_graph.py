import csv
import json
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm
import numpy as np
from pprint import pprint

def GenerateHistogram(xPoints, yPoints):
    x = np.arange(len(xPoints))
    cs=cm.Set1(np.arange(40)/20.)
    plt.bar(x, height= yPoints,  color=cs)
    plt.xticks(x+.5, xPoints)
    plt.grid(True)
    plt.savefig("test1.png")


def GeneratePieChart(xPoints, yPoints):
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    fracs = [15, 30, 45, 10]
    the_grid = GridSpec(1, 1)
    plt.subplot(the_grid[0, 0], aspect=1)
    cs=cm.Set1(np.arange(40)/5.)
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', colors=cs, shadow=True)
    plt.savefig("test2.png")


def ReadCSV(fileName, noOfRows):
    carType = []
    carCount = []
    with open(fileName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            if(count <noOfRows):
                carType.append(row[0])
                carCount.append(int(row[1]))
                count += 1
            else:
                break
    return carType, carCount

carType, carCount = ReadCSV("parking_data.csv", 10)
GenerateHistogram(carType, carCount)
GeneratePieChart(carType, carCount)