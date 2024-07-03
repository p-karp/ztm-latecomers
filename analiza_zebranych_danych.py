import pandas as pd
from datetime import datetime
import numpy as np



df = pd.read_csv('./dane_01-07_03/26-06_11:18.csv', encoding='windows-1250')

'''Zabawa'''
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
                if values[4] in St[values[2]][values[0]][values[1]].keys():
                    St[values[2]][values[0]][values[1]][values[4]].append(values[5])
                else: 
                    St[values[2]][values[0]][values[1]][values[4]] = [values[5]]
            else:
                St[values[2]][values[0]][values[1]] = {values[4]: [values[5]]}
        else:
            St[values[2]][values[0]] = {values[1]: {values[4]: [values[5]]}}
    else: 
        St[values[2]] = {values[0]: {values[1]:{values[4]: [values[5]]}}}


'''Pokaz jak to wygląda w środku'''
# print(St[523])

def statystyki(scheduledArr, file):
    scheduledDeltaArr = []
    longDelays = 0
    for i in range(len(scheduledArr)-2):
        time1 = datetime.strptime(scheduledArr[i], '%H:%M:%S').time()
        time2 = datetime.strptime(scheduledArr[i+1], '%H:%M:%S').time()
        time_diff = datetime.combine(datetime.min, time2) - datetime.combine(datetime.min, time1)
        minutes_diff = time_diff.total_seconds() / 60.0
        scheduledDeltaArr.append(minutes_diff)

    try:
        # Obliczanie interesujących nas statystyk
        mean_value = np.mean(scheduledDeltaArr)
        std_deviation = np.std(scheduledDeltaArr)
        min_value = np.min(scheduledDeltaArr)
        max_value = np.max(scheduledDeltaArr)

        file.write(f"Liczba wszystkich rejestracji:{len(scheduledDeltaArr)+2}\n")
        file.write(f"Średnia: {mean_value}\n")
        #print(f"Średnia: {mean_value}")
        file.write(f"Odchylenie standardowe: {std_deviation}\n")
        #print(f"Odchylenie standardowe: {std_deviation}")
        file.write(f"Minimum: {min_value}\n")
        #print(f"Minimum: {min_value}")
        file.write(f"Maksimum: {max_value}\n")
        #print(f"Maksimum: {max_value}\n")   
    except:
        print("Nie zarejestrowano żadnych przyjazdów dla tej lini")

    # można lekko zmodyfikować o dane zebrane z api, a nie liczone na podstawie średniej zebranej
    for delta in scheduledDeltaArr:
        if(delta > mean_value + 10.0): longDelays += 1
    file.write(f"Liczba dużych opóźnień: {longDelays}\n\n")
        #print(f"Liczba dużych opóźnień: {longDelays}")

with open("analiza_danych_testowych.csv", "w") as file:
    for line in St.keys():
        for stop in St[line].keys():
            scheduledArr = []
            for nr in St[line][stop].keys():
                for date in St[line][stop][nr].keys():
                    scheduledArr = sorted(St[line][stop][nr][date])
                    #print(f"Wartości faktyczne linia:{line} przystanek:{stop} nr:{nr} dzień:{date}")
                    file.write(f"Wartości faktyczne linia:{line} przystanek:{stop} nr:{nr} dzień:{date}\n")
                    statystyki(scheduledArr, file)