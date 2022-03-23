import csv
import numpy as np
import pandas as pd
from pandas import Series
import sys
from collections import Counter

# 1. Finding percentage of fire pokemon that are at or above level 40
# open result file 1
poke1 = open("pokemon1.txt","w")
# open original csv file
pf = open("pokemonTrain.csv", "r")
# csv reader
reader = csv.reader(pf)
fire_type = 0
level_40 = 0
for r in reader:
    if r[4] == 'fire':
        fire_type += 1
        if float(r[2]) >= 40.0:
            level_40 += 1
print('Total number of fire types: ', fire_type)
print('Total number of fire types >= level 40: ', level_40)
poke1.write(str(round((level_40/fire_type)*100)))
#close write file
poke1.close()
#close original csv file
pf.close()

#2 Fill in missing type values
#open result file 2
pokeRes = open("pokemonResult.csv", "w")
df = pd.read_csv("pokemonTrain.csv")
weak_types = df['weakness'].unique()
print(df.loc[df['weakness'] == 'water'])
print(weak_types)
weakDict = {}
for ele in weak_types:
    temp = df.loc[df['weakness'] == str(ele)]
    print(ele,'\n', temp['type'].value_counts())
print(weakDict)
#print(df)

pokeRes.close()
