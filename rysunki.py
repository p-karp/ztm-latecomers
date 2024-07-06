import processing as pr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


D, S = pr.processing('./zebraneDane/dane_ok/rj_30-06.csv', './zebraneDane/dane_ok/dane_30-06.csv')





#to nie działa
def od_pory_dnia(przyjazd, rozkład):
    pora_dnia = {'ranek': [], 'przedpołudnie': [], 'popołudnie': [], 'wieczór': [], 'noc': []}
    
    for line in przyjazd.keys():
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    pom_r = rozkład[line][stop][nr][date]
                    pom_p = przyjazd[line][stop][nr][date]
                    ranek2 = []
                    przedpołudnie2 = []
                    popołudnie2 = []
                    wieczór2 = []
                    noc2 = []
                    for i in pom_r:
                        ranek = []
                        przedpołudnie = []
                        popołudnie = []
                        wieczór = []
                        noc = []
                        for j in pom_p:
                            time1 = datetime.strptime(j, '%H:%M:%S')
                            time2 = datetime.strptime(i, '%H:%M:%S')
                            time_diff =  time1 - time2
                            minutes_diff = time_diff.total_seconds() / 60.0
                            time_do_listy = np.abs(minutes_diff)
                            if time1.hour < 9: ranek.append(time_do_listy)
                            if 9 <= time1.hour < 12: przedpołudnie.append(time_do_listy)
                            if 12 <= time1.hour < 16: popołudnie.append(time_do_listy)
                            if 16 <= time1.hour < 20: wieczór.append(time_do_listy)
                            if 20 <= time1.hour : noc.append(time_do_listy)

                        ranek2.append(np.min(ranek))
                        przedpołudnie2.append(np.min(przedpołudnie))
                        popołudnie2.append(np.min(popołudnie))
                        wieczór2.append(np.min(popołudnie))
                        noc2.append(np.min(noc))

            
    pora_dnia['ranek'] = np.mean(ranek2)
    pora_dnia['przedpołudnie'] = np.mean(przedpołudnie2)
    pora_dnia['popołudnie'] = np.mean(popołudnie2)
    pora_dnia['wieczór'] = np.mean(wieczór2)
    pora_dnia['noc'] = np.mean(noc2)

    return pora_dnia
                        
                    



a = od_pory_dnia(D, S)
mosty = list(a.keys())
mosty_o= list(a.values())
    
    # Tworzenie wykresu
plt.figure(figsize=(30, 7))
plt.bar(mosty, mosty_o, color='skyblue')
plt.xlabel('Pora dnia')
plt.ylabel('Opóźnienie [min]')
plt.xticks(rotation='vertical') 
plt.title('Opóźnienie zależne od pory dnia w dniu 30.06')
plt.tight_layout()
plt.grid(True)
plt.show()