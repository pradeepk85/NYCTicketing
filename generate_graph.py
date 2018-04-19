import csv
import json
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

def GenerateHistogram(xPoints, yPoints):
    x = np.arange(len(xPoints))
    plt.bar(x, height= yPoints)
    plt.xticks(x+.5, xPoints)
    plt.grid(True)
    plt.savefig("test.png")


def ReadJson(fileName):
    dataPoints = json.load(open(fileName))
    return dataPoints

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