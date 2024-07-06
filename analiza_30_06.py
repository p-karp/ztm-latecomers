import processing as pr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


D, S = pr.processing('./zebraneDane/dane_ok/rj_30-06-beta.csv', './zebraneDane/dane_ok/dane_30-06.csv')


czas_przyjazdu = D[523]['Saska'][1]['2024-06-30']
czas_rozkłady = S[523]['Saska'][1]['2024-06-30']

def przystanki(czas_przyjazdu, czas_rozkłady):
    od_przystanku= []
    for i in czas_rozkłady:
        pom = []
        for j in czas_przyjazdu:
            time1 = datetime.strptime(j, '%H:%M:%S')
            time2 = datetime.strptime(i, '%H:%M:%S')
            time_diff =  time1 - time2
            minutes_diff = time_diff.total_seconds() / 60.0
            time_do_listy = np.abs(minutes_diff)
            pom.append(time_do_listy)
        od_przystanku.append(np.min(pom))
    
    return np.mean(od_przystanku)


a = przystanki(czas_przyjazdu, czas_rozkłady)

def od_przystanku(przyjazd, rozkład):
    przystanek = {}
    for line in przyjazd.keys():
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    przystanek[stop, nr]= przystanki(przyjazd[line][stop][nr][date], rozkład[line][stop][nr][date])


    return przystanek


b=od_przystanku(D, S)
                 

        
def od_dnia(przyjazd, rozkład):
    przystanek = {}
    for line in przyjazd.keys():
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    przystanek[date]= przystanki(przyjazd[line][stop][nr][date], rozkład[line][stop][nr][date])


    return przystanek

c = od_dnia(D, S)
print(c)


        

