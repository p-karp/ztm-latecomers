import warsaw_data_api as wawztm
import matplotlib.pyplot as plt
import numpy as np
import time
import busStops as bs
from datetime import datetime

# Funkcja pobierające dane o autobusach
def collectBusesData(ztm, linia):
    exp = True
    while(exp):
        try:
            buses = ztm.get_buses_location(line = linia)
            exp = False
        except TypeError:
            time.sleep(2)
    return buses


# Funkcja pobierające dane o tramwajach
def collectTramsData(ztm, linia):
    exp = True
    while(exp):
        try:
            trams = ztm.get_trams_location(line = linia)
            exp = False
        except TypeError:
            time.sleep(2)
    return trams
 
# Funkcja pobierające dane o rozkładach jazdy   
def collectScheduleData(ztm, przystanek):
    exp = True
    while(exp):
        try:
            schedule = ztm.get_bus_stop_schedule_by_id(przystanek[0], przystanek[1], przystanek[2])
            exp = False
        except TypeError:
            time.sleep(2)
    return schedule

'''
Tutaj określamy które przystanki i linie bierzemy pod uwagę
'''
przystanki = [("7009", "01", "182"), ("7009", "01", "143"), ("7002", "01", "517")]
#przystanki = [("3032", "01", "N31"), ("3032", "01", "N81")]

''' 
Struktura opoznienia

opoznienia = {"id_przystanku" : {"kierunek": {"nr_linii": {"nr_brygady" : {"godzina_odjazdu": ["min_odl", "czas_przyjazdu" ,"pozostale_proby"]}}}}}
'''

def main():
    # Tworzenie obiektu API
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')

    # Funkcja pobierająca dane o przystankach
    stops = bs.getBusStopsData()
    #print(stops)
    
    # Pobieranie rozkładów jazdy
    # TODO: To trzeba będzie robić każdego dnia na nowo (bo zmiany w weekend)
    
    czas = datetime.now()
    czas_str = czas.strftime('%H:%M:%S')

    opoznienia = {}
    for przystanek in przystanki:
        schedule = collectScheduleData(ztm, przystanek)
        brygady = {}
        for ride in schedule.rides:
            if ride.time <= czas_str: # TODO: CZY PATRZYMY NA PEWNO "<=" CZY ZOSTAWIAMY JAKIŚ MARGINES 
                continue
            # TODO: CZY TU KOLEJNOŚĆ OPERACJI JEST DOBRA?
            czas_przyjazdu = ride.time
            if int(czas_przyjazdu[:2]) >= 24:
                            czas_przyjazdu = f"{int(czas_przyjazdu[:2])-24}{czas_przyjazdu[2:]}"
            if ride.brigade not in brygady:
                brygady[ride.brigade] = {czas_przyjazdu : [1000000, 0, 50]} # 50 to będzie jednocześnie mniej więcej maksymalne opoźnienie
            else:
                brygady[ride.brigade][czas_przyjazdu] = [1000000, 0, 50]
        
        if przystanek[0] not in opoznienia:
            opoznienia[przystanek[0]] = {przystanek[1] : {przystanek[2] : brygady}}
        else:
            if przystanek[1] not in opoznienia[przystanek[0]]:
                opoznienia[przystanek[0]][przystanek[1]] = {przystanek[2] : brygady}
            else:
                opoznienia[przystanek[0]][przystanek[1]][przystanek[2]] = brygady
    #print(opoznienia)
    '''Uwaga: To są wartości testowe!'''
    # startowy (aktualny) czas zbierania danych w sekundach
    t = 0
    # limit czasu zbierania danych w sekundach
    ''' Docelowo tydzień''' # TODO: ZMIENIĆ na dłużej przed dziennym testem
    t_lim = 15*60   
    # krok czasowy co ile są zbierane dane w sekundach
    ''' Docelowo minuta dt = 60 lub półminuty dt = 30'''
    dt = 60
    
    limit_odl = 0.011 # TODO: Ja bym jednak dał trochę większy margines na to
    limit_prob = 5 #w minutach TODO: docelowo ma być większy
    
    # Do zapisu w csv
    kolumny = ["przystanek", "nr_przystanku", "linia", "dzień", "godzina docelowa", "godzina faktyczna"]
    nazwa_pliku = "test.csv"
    
    # główna pętla
    
    with open(nazwa_pliku, mode = 'w', newline = '') as plik:
        writer = csv.writer(plik, delimiter = ';')
        
        writer.writerow(kolumny)
        while(t <= t_lim):
            
            
            czas = datetime.now() # TODO: być może trzeba zrobić też taki czas który aktualizuje się w pętli?
            czas_str = czas.strftime('%H:%M:%S')
            
            print(f"+-----------------------+")
            print(f"-------{czas_str}----------")
            #trams = collectTramsData(ztm)
            
            for przystanek in opoznienia:
                for nr_przystanku in opoznienia[przystanek]:
                    p_nazwa, p_x, p_y = stops[przystanek][nr_przystanku]
                    p_x, p_y  = float(p_x), float(p_y)
                    #print("PRZYSTANEK: " + p_nazwa)
                    for linia in opoznienia[przystanek][nr_przystanku]:
                        #print("LINIA: " + linia)
                        buses = collectBusesData(ztm, linia)
                        for brygada in opoznienia[przystanek][nr_przystanku][linia]:
                            if(len(opoznienia[przystanek][nr_przystanku][linia][brygada]) == 0):
                                continue
                            godz_planowa = list(opoznienia[przystanek][nr_przystanku][linia][brygada].keys())[0]
                            godz_planowa_t = datetime.strptime(godz_planowa, '%H:%M:%S')
                            #print("PLANOWY PRZYJAZD: ", godz_planowa)
                            # Trzeba mieć na uwadze że raczej nie może przyjechać za wcześnie (np. 5 minut przed czasem)
                            if (godz_planowa_t.hour <= 2 and czas.hour > 10): # Nie jestem pewien czy tu dobrze (to jest case na granicy dwóch dni)
                                if ((godz_planowa_t.hour+24)*60 + godz_planowa_t.minute) - (czas.hour*60 + czas.minute) > 5:
                                    continue
                            if (godz_planowa_t.hour*60 + godz_planowa_t.minute) - (czas.hour*60 + czas.minute) > 5:
                                continue
                            opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][2] -= 1 # Zmniejszamy liczbę szans na zmniejszenie minimum
                            print(f"PRZYSTANEK: {p_nazwa} | LINIA: {linia} | ETA: {godz_planowa}")
                            for b in buses:
                                if (czas.hour*60 + czas.minute) - (b.time.hour*60 + b.time.minute) > 3:
                                    continue 
                                if(b.brigade == brygada):
                                    odl = ((p_x - b.location.latitude)**2 + (p_y - b.location.longitude)**2)**(1/2)
                                    print("Odległość: " + str(odl))
                                    # Sprawdzamy czy wjechał do okręgu od którego zaczynamy go mierzyć
                                    if odl <= limit_odl:
                                        print("Jest w okręgu!")
                                        if odl < opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][0]: # Nowa minimalna odległość
                                            print("Nowe minimum!")
                                            opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][0] = odl
                                            opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][1] = b.time
                                            opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][2] = limit_prob
                                        
                                    if opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][2] == 0:
                                        print("Czas na osiągnięcie nowego minimum minął! Zapisujemy najlepszy wynik")
                                        if(opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][1]) == 0:
                                            writer.writerow([przystanek, nr_przystanku, linia, str(czas.date()), godz_planowa, "nie zarejestrowano przyjazdu"])
                                        writer.writerow([przystanek, nr_przystanku, linia, str(czas.date()), godz_planowa, opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][1].strftime('%H:%M:%S')])
                                        plik.flush()
                                        del opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa] # TODO: Sprawdzić czy to działa
                                    break
            roznica = datetime.now() - czas
            roznica_s = 60 - roznica.seconds
            if (roznica_s > 0):
                time.sleep(roznica_s)
            t = t + dt
        


if __name__ == "__main__":
    main()
