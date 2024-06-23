import pandas as pd
from datetime import datetime
import numpy as np


'''Zabawa'''
df = pd.read_csv('./wyniki/22-06_15.csv', encoding='windows-1250')

# Filtrowanie rekordów, gdzie nazwa przystanku zaczyna się na literę "C"
filtered_df = df[df['przystanek'].str.startswith(('C', 'm'), na=False)]

grouped_df = filtered_df.groupby(['przystanek', 'nr_przystanku', 'linia']).agg({'godzina przyjazdu': 'count'}).reset_index()
grouped_df.rename(columns={'godzina przyjazdu': 'ilość przyjazdów'}, inplace=True)
# print(grouped_df)


'''Meritum'''
St = {}

for index, row in df.iterrows():
    values = row.values.tolist()

    if values[2] in St.keys():
        if values[0] in St[values[2]].keys():
            if values[1] in St[values[2]][values[0]].keys():
                St[values[2]][values[0]][values[1]].append(values[4:])
            else:
                St[values[2]][values[0]][values[1]] = [values[4:]]
        else:
            St[values[2]][values[0]] = {values[1]: [values[4:]]}
    else: 
        St[values[2]] = {values[0]: {values[1]: [values[4:]]}}


'''Pokaz jak to wygląda w środku'''
# print(St[114]["Centrum Olimpijskie"][2])


df = pd.read_csv('./busSchedules.csv', delimiter=";", encoding='windows-1250')
for index, row in df.iterrows():
    if(index > 28 and index < 40):
        values = row.values.tolist()
        St[values[2]][values[0]][values[1]][index-29].append(values[4])


# Uważam, że fajniej tak analizować:
scheduledArr = []
df = pd.read_csv('./busSchedules.csv', delimiter=";", encoding='windows-1250')
for index, row in df.iterrows():
    if(index > 28 and index < 40):
        values = row.values.tolist()
        scheduledArr.append(values[4])

def statystyki(scheduledArr):
    scheduledDeltaArr = []
    for i in range(len(scheduledArr)-2):
        time1 = datetime.strptime(scheduledArr[i], '%H:%M:%S').time()
        time2 = datetime.strptime(scheduledArr[i+1], '%H:%M:%S').time()
        time_diff = datetime.combine(datetime.min, time2) - datetime.combine(datetime.min, time1)
        minutes_diff = time_diff.total_seconds() / 60.0
        if(minutes_diff < 30): scheduledDeltaArr.append(minutes_diff)

    # Obliczanie interesujących nas statystyk
    mean_value = np.mean(scheduledDeltaArr)
    std_deviation = np.std(scheduledDeltaArr)
    min_value = np.min(scheduledDeltaArr)
    max_value = np.max(scheduledDeltaArr)

    print(f"Średnia: {mean_value}")
    print(f"Odchylenie standardowe: {std_deviation}")
    print(f"Minimum: {min_value}")
    print(f"Maksimum: {max_value}\n")

print("Wartości oczekiwane:")
statystyki(scheduledArr)

scheduledArr = []
for i in range(len(St[114]["Centrum Olimpijskie"][2])):
    scheduledArr.append(St[114]["Centrum Olimpijskie"][2][i][1])

print("Wartości faktyczne:")
statystyki(scheduledArr)