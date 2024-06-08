import warsaw_data_api as wawztm
import matplotlib.pyplot as plt
import numpy as np
import time
import busStops as bs


# Funkcja pobierające dane o autobusach
def collectBusesData(ztm):
    exp = True
    while(exp):
        try:
            buses = ztm.get_buses_location()
            exp = False
        except TypeError:
            time.sleep(2)
    return buses


# Funkcja pobierające dane o tramwajach
def collectTramsData(ztm):
    exp = True
    while(exp):
        try:
            trams = ztm.get_trams_location()
            exp = False
        except TypeError:
            time.sleep(2)
    return trams


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


def main():
    # Tworzenie obiektu API
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')

    # Funkcja pobierająca dane o przystankach
    stops = bs.getBusStopsData()
    print(stops)

    '''Uwaga: To są wartości testowe!'''
    # startowy (aktualny) czas zbierania danych w sekundach
    t = 0
    # limit czasu zbierania danych w sekundach
    ''' Docelowo tydzień'''
    t_lim = 30        
    # krok czasowy co ile są zbierane dane w sekundach
    ''' Docelowo minuta dt = 60 lub półminuty dt = 30'''
    dt = 10   

    # główna pętla
    while(t <= t_lim):
        buses = collectBusesData(ztm)
        trams = collectTramsData(ztm)

        # obliczanie ETA 
        for bus in buses:
            calculateETA(bus)
        for tram in trams:
            calculateETA(tram)

        print(t)
        time.sleep(dt)
        t = t + dt


if __name__ == "__main__":
    main()