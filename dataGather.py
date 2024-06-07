import warsaw_data_api as wawztm
import matplotlib.pyplot as plt
import numpy as np
import time
import findAllBusStops


# Funkcja pobierająca dane o przystankach
def collectstops(ztm):
    '''
    dodać strukturę z danymi przysanków
    zapisać przysatnki w tej strukturze
    '''
    line = "519"
    print(findAllBusStops.findAllBusStops(line))

# Funkcja pobierające dane o autobusach
def collectBusesData(ztm):
    exp = True
    while(exp):
        try:
            buses = ztm.get_buses_location()
            exp = False
        except TypeError:
            time.sleep(200)
    return buses


# Funkcja pobierające dane o tramwajach
def collectTramsData(ztm):
    exp = True
    while(exp):
        try:
            trams = ztm.get_trams_location()
            exp = False
        except TypeError:
            time.sleep(200)
    return trams


# Funkcja obliczająca opóźnienie autobusu
def calculateETA(veh):

    '''dodać logikę'''
    print("numer pojazdu ", veh.vehicle_number)
    print("numer linii ", veh.lines)
    print("szerokość geograficzna: ", veh.location.latitude)
    print("długość geograficzna: ", veh.location.longitude)
    print("---")


def main():
    # Tworzenie obiektu API
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')


    stops = collectstops(ztm)
    buses = collectBusesData(ztm)
    trams = collectTramsData(ztm)

    # obliczanie ETA 
    for bus in buses:
        calculateETA(bus)
    for tram in trams:
        calculateETA(tram)

    '''stworzyć pętlę '''
if __name__ == "__main__":
    main()