#Tommy Cho

import csv
import re
from collections import Counter

# ----- COVID-19 DATASET PROBLEM -----


def dateSwapper(dateList):
# Helper method that swaps the month and day of a split list of date items
# parameter dateList: a date in the form of a list (e.g. ['15', '02', '2001'])
# return: a date in the form of a list (e.g. ['02', '15', '2001'])
    dateList[0], dateList[1] = dateList[1], dateList[0]
    return dateList

def latitudeAvg(province):
# Helper method to find the average latitude of a province
# parameter province: string of a province that we want to find the average latitude of
# return: the average latitude of a province rounded to 2 decimal points
    lat_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == province: 
                if row[6] != "NaN":
                    lat_list.append(float(row[6])) #list of all latitudes that are not 'NaN' in the province
    return round((sum(lat_list) / len(lat_list)),2) #taking the average and rounding

def longitudeAvg(province):
# Helper method to find the average longitude of a province
# parameter province: string of a province that we want to find the average longitude of
# return: the average longitude of a province rounded to 2 decimal points
    lon_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == province:
                if row[7] != "NaN":
                    lon_list.append(float(row[7])) #list of all longitudes that are not 'NaN' in the province
    return round((sum(lon_list) / len(lon_list)),2) #taking the average and rounding

def commonCity(province):
# Helper method that finds the most common city in a province, ties will be broken alphabetically
# parameter province: string of a province that we want to find the most common city of
# return: String of the most common city of a province
    city_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == province:
                if row[3] != "NaN":   
                    city_list.append(row[3]) #list of all the cities in the province
        #sorted list of most common cities. sorted by value, then alphabetically
        citySorted = (sorted(Counter(city_list).most_common(), key=lambda x: (-x[1], x[0]))) 
        return citySorted[0][0]
    
def symptomsHelper(province):
# Helper method that finds the most common sympyom in a province, ties will be broken alphabetically 
# parameter province: string of a province that we want to find the most common symptom of
# return: String of the most common symptom of a province
    symptom_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            i = 0
            if row[4] == province:
                if row[11] != "NaN":   
                    temp = row[11].strip('').split(';')
                    symptom_list.extend([s.strip() for s in temp]) #list of all symptoms in the province
        while i < len(symptom_list):
            if re.match('fever.+', symptom_list[i]): #handles case where the specific temperature of a fever is listed
                symptom_list[i] = 'fever' #counts items such as 'fever 38C' as just 'fever'
            i = i+1
        #sorted list of most common symptoms. sorted by value, then alphabetically
        symptomSorted = (sorted(Counter(symptom_list).most_common(), key=lambda x: (-x[1], x[0])))
        return symptomSorted[0][0]

#main code to run
with open('covidResult.csv', 'w', newline='') as outFile:
    writer = csv.writer(outFile, delimiter=',')
    with open('covidTrain.csv') as covidfile:
        reader = csv.reader(covidfile)
        writer.writerow(next(reader))
        for row in reader:
        # 2.1 Rounded Age 
            if re.match('[0-9]+-[0-9]+', row[1]): #match any item with two numbers and a dash between them
                temp = [int(n) for n in row[1].split('-')]
                row[1] = round(sum(temp)/2)
        # 2.2 Date Formatting
            row[8] = ".".join(dateSwapper(row[8].split('.')))
            row[9] = ".".join(dateSwapper(row[8].split('.')))
            row[10] = ".".join(dateSwapper(row[8].split('.')))
        # 2.3 Longitutde and Latitude Values
            if re.match('NaN', row[6]):
                row[6] = latitudeAvg(row[4])
            if re.match('NaN', row[7]):
                row[7] = longitudeAvg(row[4])
        # 2.4 Missing City Values
            if re.match('NaN', row[3]):
                row[3] = commonCity(row[4])
        # 2.5 Missing Symptom Values
            if re.match('NaN', row[11]):
                row[11] = symptomsHelper(row[4])
            writer.writerow(row)

            