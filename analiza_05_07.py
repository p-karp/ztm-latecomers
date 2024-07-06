import processing as pr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


D, S = pr.processing('./zebraneDane/dane_ok/rj_05-07.csv', './zebraneDane/dane_ok/dane_05-07.csv')




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




def od_przystanku(przyjazd, rozkład):
    przystanek = {}
    for line in przyjazd.keys():
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    przystanek[stop +' '+ str(nr)]= przystanki(przyjazd[line][stop][nr][date], rozkład[line][stop][nr][date])


    return przystanek


b=od_przystanku(D, S)
przystankii= list(b.keys())
przystanki_o= list(b.values())
    
    # Tworzenie wykresu
plt.figure(figsize=(30, 7))
plt.bar(przystankii, przystanki_o, color='skyblue')
plt.xlabel('Przystanki')
plt.ylabel('Opóźnienie [min]')
plt.xticks(rotation='vertical') 
plt.title('Opóźnienie dla danego przystanku w dniu 30.06')
plt.tight_layout()
plt.grid(True)
plt.show()

                 

        
def od_dnia(przyjazd, rozkład):
    przystanek = {}
    for line in przyjazd.keys():
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    przystanek[date]= przystanki(przyjazd[line][stop][nr][date], rozkład[line][stop][nr][date])


    return przystanek

c = od_dnia(D, S)
dzień= list(c.keys())
dzień_o= list(c.values())
    
    # Tworzenie wykresu
plt.figure()
plt.bar(dzień, dzień_o, color='skyblue')
plt.xlabel('Data')
plt.ylabel('Opóźnienie [min]')
plt.xticks(rotation='vertical') 
plt.title('Opóźnienie w dniu 30.06')
plt.tight_layout()
plt.grid(True)
plt.show()



        
def od_linii(przyjazd, rozkład):
    przystanek = {}
    for line in przyjazd.keys():
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    przystanek[str(line)]= przystanki(przyjazd[line][stop][nr][date], rozkład[line][stop][nr][date])


    return przystanek

d = od_linii(D, S)

linia = list(d.keys())
linia_o= list(d.values())
    
    # Tworzenie wykresu
plt.figure(figsize=(30, 7))
plt.bar(linia, linia_o, color='skyblue')
plt.xlabel('Numery Linii')
plt.ylabel('Opóźnienie [min]')
plt.xticks(rotation='vertical') 
plt.title('Opóźnienie dla danej linii w dniu 30.06')
plt.tight_layout()
plt.grid(True)
plt.show()


def od_mostu(przyjazd, rozkład):
    przystanek = {'most Grota - Roweckiego': [], 'most Gdański': [], 'most Śląsko - Dąbrowski':[], 'most Świętokrzyski':[], 'most Poniatowskiego':[], 'most Łazienkowski':[], 'most Siekierkowski': []}
    for line in przyjazd.keys():
        if line == 114:
             klucz = 'most Grota - Roweckiego'
        if line == 500 or line == 6:
             klucz = 'most Gdański'
        if line == 190 or line == 26:
             klucz = 'most Śląsko - Dąbrowski'
        if line == 162:
            klucz = 'most Świętokrzyski'
        if line == 9 or line == 521:
             klucz = 'most Poniatowskiego'
        if line == 523:
             klucz = 'most Łazienkowski'
        if line == 148:
             klucz = 'most Siekierkowski'
        for stop in przyjazd[line].keys():
            for nr in przyjazd[line][stop].keys():
                for date in przyjazd[line][stop][nr].keys():
                    przystanek[klucz]= przystanki(przyjazd[line][stop][nr][date], rozkład[line][stop][nr][date])


    return przystanek


e = od_mostu(D, S)
mosty = list(e.keys())
mosty_o= list(e.values())
    
    # Tworzenie wykresu
plt.figure(figsize=(30, 7))
plt.bar(mosty, mosty_o, color='skyblue')
plt.xlabel('Nazwa mostu')
plt.ylabel('Opóźnienie [min]')
plt.xticks(rotation='vertical') 
plt.title('Opóźnienie dla danego mostu w dniu 30.06')
plt.tight_layout()
plt.grid(True)
plt.show()



#to nie działa
def od_pory_dnia(przyjazd, rozkład):
    pora_dnia = {'ranek': [], 'przedpołudnie': [], 'popołudnie': [], 'wieczór': [], 'noc': []}
    ranek = []
    przedpołudnie = []
    popołudnie = []
    wieczór = []
    noc = []
    for line in rozkład.keys():
        for stop in rozkład[line].keys():
            for nr in rozkład[line][stop].keys():
                for date in rozkład[line][stop][nr].keys():
                    pom = rozkład[line][stop][nr][date]
                    lista2 = []
                    for i in pom:
                        lista = []
                        for j in przyjazd[line][stop][nr][date]:
                            time1 = datetime.strptime(j, '%H:%M:%S')
                            time2 = datetime.strptime(i, '%H:%M:%S')
                            time_diff =  time1 - time2
                            minutes_diff = time_diff.total_seconds() / 60.0
                            time_do_listy = np.abs(minutes_diff)
                            lista.append(time_do_listy)
                        lista2.append(np.min(lista))
                        if time1.hour < 6:
                            ranek.append
                        
                    
                    


