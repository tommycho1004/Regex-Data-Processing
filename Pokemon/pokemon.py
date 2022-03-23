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
print(df.loc[df['type'] == np.nan])
# a dict mapping the most common type to weakness
weakDict = {}
for ele in weak_types:
    # find the rows with specified weakness and find the most common type => presort the df
    temp = df.loc[df['weakness'] == str(ele)].sort_values(by='type')
    weakDict[ele] = temp['type'].value_counts()[:1].index[0]
    print(ele,'\n', temp['type'].value_counts()[:1].index[0])
# replace all NaN values in type with corresponding weakness according to the weakness Dictionary
for key in weakDict.keys():
    df.loc[df['type'].isnull() & (df['weakness'] == key), 'type'] = weakDict[key]
print(df)

#3 replace missing ATK/HP/DEF values with mean() when > lv40 or <= lv40. Using the same df as #2
df.to_csv('pokemonResult.csv', index=False)
pokeRes.close()
