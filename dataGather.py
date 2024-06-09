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


# Funkcja obliczająca opóźnienie pojazdu
def calculateETA(veh):
    '''dodać logikę

    funkcja zapisuje do pliku z dnia nowe rekordy po dojechaniu autobusu do przystanku w postaci:
    | ID | nazwa przystanku | numer przystanku | nr linii | dzień | czas planowego przybycia | czas faktycznego przybycia |
    '''

    print("numer pojazdu ", veh.vehicle_number)
    print("numer linii ", veh.lines)
    print("szerokość geograficzna: ", veh.location.latitude)
    print("długość geograficzna: ", veh.location.longitude)
    print("---")

'''
Tutaj określamy które przystanki i linie bierzemy pod uwagę
'''
#przystanki = [("7009", "01", "182"), ("7009", "01", "143"), ("7002", "01", "517"), ("7002", "01", "N24")]
przystanki = [("3032", "01", "N31"), ("3032", "01", "N81")]

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
    ''' To trzeba będzie robić każdego dnia na nowo (bo zmiany w weekend) '''
    
    czas = datetime.now().strftime('%H:%M:%S')

    opoznienia = {}
    for przystanek in przystanki:
        schedule = collectScheduleData(ztm, przystanek)
        brygady = {}
        for ride in schedule.rides:
            if ride.time <= czas:
                continue
            if ride.brigade not in brygady:
                brygady[ride.brigade] = {ride.time : [1000000, 0, 10]}
            else:
                brygady[ride.brigade][ride.time] = [1000000, 0, 10]
        
        if przystanek[0] not in opoznienia:
            opoznienia[przystanek[0]] = {przystanek[1] : {przystanek[2] : brygady}}
        else:
            if przystanek[1] not in opoznienia[przystanek[0]]:
                opoznienia[przystanek[0]][przystanek[1]] = {przystanek[2] : brygady}
            else:
                opoznienia[przystanek[0]][przystanek[1]][przystanek[2]] = brygady
    print(opoznienia)
    '''Uwaga: To są wartości testowe!'''
    # startowy (aktualny) czas zbierania danych w sekundach
    t = 0
    # limit czasu zbierania danych w sekundach
    ''' Docelowo tydzień'''
    t_lim = 30        
    # krok czasowy co ile są zbierane dane w sekundach
    ''' Docelowo minuta dt = 60 lub półminuty dt = 30'''
    dt = 10   
    
    limit_odl = 0.011
    limit_czasu = 15 #w minutach
    
    
    # główna pętla
    while(t <= t_lim):
        
        
        #trams = collectTramsData(ztm)
        
        for przystanek in opoznienia:
            for nr_przystanku in opoznienia[przystanek]:
                p_nazwa, p_x, p_y = stops[przystanek][nr_przystanku]
                for linia in opoznienia[przystanek][nr_przystanku]:
                    buses = collectBusesData(ztm, linia)
                    for brygada in opoznienia[przystanek][nr_przystanku][linia]:
                        godz_planowa = list(opoznienia[przystanek][nr_przystanku][linia][brygada].keys())[0]
                        godz_planowa_popr = f"{int(godz_planowa[:2])-24}{godz_planowa[2:]}" # TODO: NA POZIOMIE ZAPISYWANIA W OPOZNIENIACH (?)
                        print(godz_planowa_popr)
                        for b in buses:
                            # TODO: aktualny - b.time < 3 minut żeby brać pod uwagę
                            if(b.brigade == brygada):
                                print(b.time)
                        
                        # TODO: zapisywanie do pliku
                        #del opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa]
                        
            
        break
        # obliczanie ETA
        ''' 
        for bus in buses:
            calculateETA(bus)
        for tram in trams:
            calculateETA(tram)
        '''
        # TODO: obliczyć kiedy wykonać następne zapytanie
        time.sleep(dt)
        t = t + dt


if __name__ == "__main__":
    main()
