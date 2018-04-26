import csv
import json
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm
import numpy as np
from pprint import pprint

def GenerateHistogram(xPoints, yPoints, title, xlable, ylabel, fileName):
    x = np.arange(len(xPoints))
    cs=cm.Set1(np.arange(40)/2.)
    plt.bar(x, height= yPoints,  color=cs)
    plt.xticks(x+.5, xPoints)
    plt.grid(True)
    plt.title(title)
    plt.xlabel(xlable)
    plt.ylabel(ylabel)
    plt.savefig(fileName)


def GeneratePieChart(label, values, title, fileName):
    labels = label
    fracs = values
    the_grid = GridSpec(1, 1)
    plt.subplot(the_grid[0, 0], aspect=1)
    cs=cm.Set1(np.arange(40)/5.)
    plt.pie(fracs, labels=labels, autopct='%1.1f%%', colors=cs, shadow=True)
    plt.title(title)
    plt.savefig(fileName)


def ReadCSV(fileName, noOfRows):
    vehicleType = []
    vehicleCount = []
    with open(fileName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        for row in readCSV:
            if(count <noOfRows):
                vehicleType.append(row[0])
                vehicleCount.append(int(row[1]))
                count += 1
            else:
                break
    return vehicleType, vehicleCount

def getPieChartData(fileName, noOfPoints):
    with open(fileName) as csvfile:
        readCSV = csv. reader(csvfile, delimiter=',')
        count = 0.0
        totalCount = 0.0
        tempValue = []
        pieChartLabel = []
        pieChartValue = []
        for row in readCSV:
            if(count <noOfPoints):
                pieChartLabel.append(row[0])
                tempValue.append(float(row[1]))
                count += 1
            totalCount += float(row[1])
        count = 0.0
        for val in tempValue:
            count += (val/totalCount)*100
            pieChartValue.append(format((val/totalCount)*100, '.2f'))
        pieChartLabel.append("Others")
        pieChartValue.append(100.0-count)
        return pieChartLabel, pieChartValue


countyCode, vehicleCount = ReadCSV("Part-1.csv", 10)
GenerateHistogram(countyCode, vehicleCount, 'NYC: Parking Tickets Based on Location', 'County Code', 'Ticket Count(1e^7)', 'nyc_pt_location.png')
vehicleType, vehicleCount = ReadCSV("Part-2.csv", 10)
GenerateHistogram(vehicleType, vehicleCount, 'NYC: Parking Tickets Based on Vehicle Type', 'Vehicle Type', 'Ticket Count(1e^7)', 'nyc_pt_vehicle_type.png')
# plateType, vehicleCount = ReadCSV("Part-3.csv", 10)
# GenerateHistogram(plateType, vehicleCount, 'NYC: Parking Tickets Based on Plate Type', 'Plate Type', 'Ticket Count(1e^7)', 'nyc_pt_plate_type.png')

pieChartLabel, pieChartValue = getPieChartData("Part-3.csv", 3)
GeneratePieChart(pieChartLabel, pieChartValue, 'NYC: Parking Tickets Based on Plate Type', 'nyc_pt_plate_type.png')
