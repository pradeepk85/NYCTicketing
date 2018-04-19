import json
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

def GenerateHistogram(xPoints, yPoints):
    # x = np.random.normal(size = 1000)
    x = np.arange(len(xPoints))
    plt.bar(x, height= yPoints)
    plt.xticks(x+.5, xPoints)
    plt.grid(True)
    plt.savefig("test.png")


def ReadJson(fileName):
    dataPoints = json.load(open(fileName))
    return dataPoints

def ReturnDataPoints(dict):
    carType = []
    carCount = []
    vehicleDetails = dict["type"]
    for vehicle in vehicleDetails:
        carType.append(vehicle["VehicleBodyType"])
        carCount.append(vehicle["count"])
    return carType, carCount

dataPoints = ReadJson("output.json")
carType, carCount = ReturnDataPoints(dataPoints)
GenerateHistogram(carType, carCount)