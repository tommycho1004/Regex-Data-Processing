import csv
import numpy as np
import pandas as pd
from pandas import Series
import sys
from collections import Counter
import json

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
#print('Total number of fire types: ', fire_type)
#print('Total number of fire types >= level 40: ', level_40)
poke1.write(str(round((level_40/fire_type)*100)))
#close write file
poke1.close()
#close original csv file
pf.close()

#2 Fill in missing type values
#open result file 2
pokeRes = open("pokemonResult.csv", "w")
df = pd.read_csv("pokemonTrain.csv")
#getting unique weakness keys
weak_types = df['weakness'].unique()
# df.loc[cond, column to modify]
#print(df.loc[df['level'] <= 40])
# a dict mapping the most common type to weakness
weakDict = {}
for ele in weak_types:
    # find the rows with specified weakness and find the most common type => presort the df so its alphabetical
    temp = df.loc[df['weakness'] == str(ele)].sort_values(by='type')
    weakDict[ele] = temp['type'].value_counts()[:1].index[0]
    #print(ele,'\n', temp['type'].value_counts()[:1].index[0])
# replace all NaN values in type with corresponding weakness according to the weakness Dictionary
for key in weakDict.keys():
    df.loc[df['type'].isnull() & (df['weakness'] == key), 'type'] = weakDict[key]
#print(df)

# 3 replace missing ATK/HP/DEF values with mean() when > lv40 or <= lv40. Using the same df as #2
# round to 1 decimal
lv_thresh = 40.0
avg_ATK_above = round(df.loc[df['level'] > lv_thresh, 'atk'].mean(),1)
avg_ATK_below = round(df.loc[df['level'] <= lv_thresh, 'atk'].mean(),1)
avg_HP_above = round(df.loc[df['level'] > lv_thresh, 'hp'].mean(),1)
avg_HP_below = round(df.loc[df['level'] <= lv_thresh, 'hp'].mean(),1)
avg_DEF_above = round(df.loc[df['level'] > lv_thresh, 'def'].mean(),1)
avg_DEF_below = round(df.loc[df['level'] <= lv_thresh, 'def'].mean(),1)
#print(avg_ATK_above, avg_ATK_below, avg_HP_above, avg_HP_below, avg_DEF_above, avg_DEF_below)
#ATK
df.loc[df['atk'].isnull() & (df['level'] > lv_thresh), 'atk'] = avg_ATK_above
df.loc[df['atk'].isnull() & (df['level'] <= lv_thresh), 'atk'] = avg_ATK_below
#HP
df.loc[df['hp'].isnull() & (df['level'] > lv_thresh), 'hp'] = avg_HP_above
df.loc[df['hp'].isnull() & (df['level'] <= lv_thresh), 'hp'] = avg_HP_below
#DEF
df.loc[df['def'].isnull() & (df['level'] > lv_thresh), 'def'] = avg_DEF_above
df.loc[df['def'].isnull() & (df['level'] <= lv_thresh), 'def'] = avg_DEF_below
df.to_csv('pokemonResult.csv', index=False)
#close file
pokeRes.close()
# 4 Create pokemon personality dictionary from i:pokemonResult.csv -> o: pokemon4.txt
# can use df from #3, but cuz of the instructions ill make a new df
# result file 4

df2 = pd.read_csv('pokemonResult.csv')
# list of all types
all_types = df2['type'].unique()
all_types.sort()
#print(all_types)
result = {}
for ele in all_types:
    temp = df2.loc[df2['type'] == ele, 'personality'].unique()
    temp = temp.tolist()
    temp.sort()
    result[ele] = temp
#close result file
with open('pokemon4.txt','w') as poke4:
    for key, value in result.items():
        poke4.write("{}: {}\n".format(key, str(value).strip('[]').replace("'", '')))
poke4.close()

#5
df3 = pd.read_csv('pokemonResult.csv')
avg_hp_3 = round(df.loc[df['stage'] == 3.0, 'hp'].mean())
with open('pokemon5.txt','w') as poke5:
    poke5.write(str(avg_hp_3))
poke5.close()