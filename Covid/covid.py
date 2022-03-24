import csv
import re
from collections import Counter

def dateSwapper(dateList):
    dateList[0], dateList[1] = dateList[1], dateList[0]
    return dateList

def latitudeAvg(province):
    lat_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == province:
                if row[6] != "NaN":
                    lat_list.append(float(row[6]))
    return round((sum(lat_list) / len(lat_list)),2)

def longitudeAvg(province):
    lon_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == province:
                if row[7] != "NaN":
                    lon_list.append(float(row[7]))
    return round((sum(lon_list) / len(lon_list)),2)

def commonCity(province):
    city_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == province:
                if row[3] != "NaN":   
                    city_list.append(row[3])
        citySorted = (sorted(Counter(city_list).most_common(), key=lambda x: (-x[1], x[0])))
        return citySorted[0][0]
    
def symptomsHelper(province):
    symptom_list = []
    with open('covidTrain.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            i = 0
            if row[4] == province:
                if row[11] != "NaN":   
                    temp = row[11].strip('').split(';')
                    symptom_list.extend([s.strip() for s in temp])
        while i < len(symptom_list):
            if re.match('fever.+', symptom_list[i]):
                symptom_list[i] = 'fever'
            i = i+1
        symptomSorted = (sorted(Counter(symptom_list).most_common(), key=lambda x: (-x[1], x[0])))
        return symptomSorted[0][0]

with open('covidTrain.csv') as covidfile:
    reader = csv.reader(covidfile)
    next(reader)
    for row in reader:
        if re.match('[0-9]+-[0-9]+', row[1]):
            temp = [int(n) for n in row[1].split('-')]
            row[1] = round(sum(temp)/2)
            #print(row[1])
        row[8] = ".".join(dateSwapper(row[8].split('.')))
        row[9] = ".".join(dateSwapper(row[8].split('.')))
        row[10] = ".".join(dateSwapper(row[8].split('.')))
        if re.match('NaN', row[6]):
            row[6] = latitudeAvg(row[4])
        if re.match('NaN', row[7]):
            row[7] = longitudeAvg(row[4])
        if re.match('NaN', row[3]):
            row[3] = commonCity(row[4])
        if re.match('NaN', row[11]):
            row[11] = symptomsHelper(row[4])
            