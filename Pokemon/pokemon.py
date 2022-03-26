# Jennifer Xin
import csv
import sys
from collections import Counter
import math
from collections import defaultdict

# 1. Finding percentage of fire pokemon that are at or above level 40
# open result file 1
poke1 = open("pokemon1.txt", "w")
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
# print('Total number of fire types: ', fire_type)
# print('Total number of fire types >= level 40: ', level_40)
value = str(round((level_40 / fire_type) * 100))
L = ['Percentage of fire type Pokemons at or above level 40 = ', value]
poke1.writelines(L)
# close write file
poke1.close()
# close original csv file
pf.close()

# 2 Fill in missing type values
# open result file 2
# not using pandas is pain
pf = open("pokemonTrain.csv", "r")
reader2 = csv.reader(pf)
weak_types = []
for row in reader2:
    if row[5] not in weak_types:
        weak_types.append(row[5])
weak_types = weak_types[1:]
weak_types.sort()
pf.close()
type_mapping = {}
for ele in weak_types:
    filtered = []
    pf = open("pokemonTrain.csv", "r")
    reader2 = csv.reader(pf)
    for row in reader2:
        if row[5] == ele:
            filtered.append(row[4])
    filtered.sort()
    filtered = [x for x in filtered if x != 'NaN']
    type_mapping[ele] = Counter(filtered).most_common(1)[0][0]
    pf.close()
#print(type_mapping)

# 3 replace missing ATK/HP/DEF values with avg when > lv40 or <= lv40.
# round to 1 decimal
pf = open("pokemonTrain.csv", "r")
reader = csv.reader(pf)
next(reader)
avg_atk_above = 0.0
aac = 0.0
avg_atk_below = 0.0
abc = 0.0
avg_hp_above = 0.0
hac = 0
avg_hp_below = 0.0
hbc = 0
avg_def_above = 0.0
dac = 0
avg_def_below = 0.0
dbc = 0
lv_thresh = 40.0
for row in reader:
    if float(row[2]) > lv_thresh:
        if row[6] != 'NaN':
            avg_atk_above += float(row[6])
            aac += 1
        if row[7] != 'NaN':
            avg_def_above += float(row[7])
            dac += 1
        if row[8] != 'NaN':
            avg_hp_above += float(row[8])
            hac += 1
    elif float(row[2]) <= lv_thresh:
        if row[6] != 'NaN':
            avg_atk_below += float(row[6])
            abc += 1
        if row[7] != 'NaN':
            avg_def_below += float(row[7])
            dbc += 1
        if row[8] != 'NaN':
            avg_hp_below += float(row[8])
            hbc += 1
avg_atk_above = round(avg_atk_above / aac, 1)
avg_atk_below = round(avg_atk_below / abc, 1)
avg_def_above = round(avg_def_above / dac, 1)
avg_def_below = round(avg_def_below / dbc, 1)
avg_hp_above = round(avg_hp_above / hac, 1)
avg_hp_below = round(avg_hp_below / hbc, 1)
r = open('pokemonResult.csv', 'w', newline='')
res = csv.writer(r, delimiter=',')
pf = open("pokemonTrain.csv", "r")
reader2 = csv.reader(pf)
for row in reader2:
    if row[4] == 'NaN': #3 type - weakness matching
        row[4] = type_mapping[row[5]]
    if row[6] == 'NaN':
        if float(row[2]) > lv_thresh:
            row[6] = avg_atk_above
        else:
            row[6] = avg_atk_below
    if row[7] == 'NaN':
        if float(row[2]) > lv_thresh:
            row[7] = avg_def_above
        else:
            row[7] = avg_def_below
    if row[8] == 'NaN':
        if float(row[2]) > lv_thresh:
            row[8] = avg_hp_above
        else:
            row[8] = avg_hp_below
    res.writerow(row)
r.close()
pf.close()

# 4 Create a dictionary mapping pokemon types to personalities alphabetically
pf = open("pokemonResult.csv", "r")
reader = csv.reader(pf)
next(reader)
personality = defaultdict(list)
# creating a dictionary that maps all unique types with unique personalities
for row in reader:
    if row[4] not in personality:
        personality[row[4]].append(row[3])
    else:
        if str(row[3]) not in personality[row[4]]:
            personality[row[4]].append(row[3])
# sort alphabetically
for i in personality:
    temp = personality[i]
    temp.sort()
    personality[i] = temp
# write with correct formatting
with open('pokemon4.txt','w') as poke4:
    poke4.write('Pokemon type to personality mapping:\n\n')
    for i in sorted(personality):
        poke4.write("\t{}: {}\n".format(i, str(personality[i]).strip('[]').replace("'",'')))
poke4.close()
pf.close()
#5
pf = open("pokemonResult.csv", "r")
reader = csv.reader(pf)
next(reader)
avg_hp = 0
count = 0
# calculating avg_hp for 3.0 pokemons
for row in reader:
    if float(row[9]) == 3.0:
        avg_hp += float(row[8])
        count += 1
avg_hp = str(round(avg_hp / count))
# write with correct format
with open('pokemon5.txt','w') as poke5:
    L = ['Average hit point for Pokemons of stage 3.0 = ', avg_hp]
    poke5.writelines(L)
poke5.close()
pf.close()
