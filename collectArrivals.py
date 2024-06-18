import warsaw_data_api as wawztm
import time
import busStops as bs
from datetime import datetime
import csv
import os

# Funkcja pobierające dane o autobusach
def collectBusesData(ztm):
    exp = True
    while(exp):
        try:
            buses = ztm.get_buses_location()
            exp = False
        except Exception as e:
            time.sleep(2)
            #print(f"Zwrócono wyjątek: {e}")
    return buses

# Funkcja pobierające dane o tramwajach
def collectTramsData(ztm):
    exp = True
    while(exp):
        try:
            trams = ztm.get_trams_location()
            exp = False
        except Exception as e:
            time.sleep(2)
            #print(f"Zwrócono wyjątek: {e}")
    return trams
    
# przystanki: {"LINIA": {"KIERUNEK": [(id_przystanku, nr_przystanku), ... ]}}
przystanki = {"114": {"UKSW": [('1162', '06'), ('1159', '01'), ('1013', '03'), ('6083', '01'), ('6099', '02'), ('6003', '06'), ('6098', '02')], 
"Bródno Podgrodzie": [('6003', '05'), ('6099', '01'), ('6096', '02'), ('6083', '02'), ('1013', '04'), ('1159', '02'), ('1158', '01')]}}
    
def main():
    # Tworzenie obiektu API
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
    
    # Funkcja pobierająca dane o przystankach
    stops = bs.getBusStopsData()

    czas = datetime.now()   
    czas_str = czas.strftime('%H:%M:%S')
    
    # tracked_veh: {"LINIA": {"BRYGADA": ["prawidłowy kierunek", {"KIERUNEK1": [(min_odleglosc_od_przystanku, czas_osiagniecia_minimum, pozostale_proby)], "KIERUNEK2": [...]}}}]
    tracked_veh = {}
    for linia in przystanki:
        tracked_veh[linia] = {}
    
    # startowy (aktualny) czas zbierania danych w sekundach
    t = 0
    
    # krok czasowy co ile są zbierane dane (w sekundach)
    dt = 10
    
    # promień okręgu (w stopniach), kiedy jest łapany autobus
    limit_odl = 0.005 # Około pół kilometra
    
    # Liczba prób na znalezienie nowego minimum (i też na wjechanie do nowego okręgu)
    limit_prob = 6*15 # 15 minut TODO: zrobić większe potem
    # Liczba prób dla ostatnich przystanków na trasie
    limit_prob_gr = 6*2 # 2 miniuty
    
    # Do zapisu w csv
    kolumny = ["przystanek", "nr_przystanku", "linia", "kierunek", "dzień", "godzina przyjazdu"]
    nazwa_pliku = f"wyniki/{czas.strftime('%d-%m_%H:%M')}.csv"
    
    # Główna pętla programu
    with open(nazwa_pliku, mode = 'w', newline = '') as plik:
        writer = csv.writer(plik, delimiter = ',')
        writer.writerow(kolumny)
        
        while(True):
            czas = datetime.now()
            czas_str = czas.strftime('%H:%M:%S')
            
            print(f"+-----------------------+")
            print(f"-------{czas_str}----------")
            
            # Tworzymy słownik vehicles, w którym przechowujemy zlokalizowane busy, podzielone na linie i brygady
            # {'517': {'3': veh, '7':veh}, ...}
            vehicles = {}
            
            buses = collectBusesData(ztm)
            trams = collectTramsData(ztm)
            
            for veh in (buses+trams):
                if veh.lines not in przystanki:
                    continue
                if veh.lines not in vehicles:
                    vehicles[veh.lines] = {}
                # Jeżeli było dwa lub więcej autobusów z tej samej brygady, to bierzemy tylko ten z największym czasem
                if veh.brigade in vehicles[veh.lines]:
                    if veh.time < vehicles[veh.lines][veh.brigade].time:
                        continue
                vehicles[veh.lines][veh.brigade] = veh
            
            for veh_l in vehicles:
                for veh_b in vehicles[veh_l]:
                    zapamietaj = 0
                    kierunki = list(przystanki[veh_l].keys())
                    if veh_b not in tracked_veh[veh_l]:
                        tracked_veh[veh_l][veh_b] = {kierunki[0]: [[1000, 0, -1] for _ in przystanki[veh_l][kierunki[0]]], kierunki[1]: [[1000, 0, -1] for _ in przystanki[veh_l][kierunki[1]]]}
                    statusy = {kierunki[0]:-2,kierunki[1]: -2}
                    statusy_cz = {kierunki[0]:[0,0],kierunki[1]: [0,0]}
                    for kier in tracked_veh[veh_l][veh_b]:
                        status = -1
                        for i, przystanek in enumerate(przystanki[veh_l][kier]):
                            if(tracked_veh[veh_l][veh_b][kier][i][2] != -1):
                                status = tracked_veh[veh_l][veh_b][kier][i][2]
                                statusy_cz[kier] = [i, tracked_veh[veh_l][veh_b][kier][i][1]]
                            if(tracked_veh[veh_l][veh_b][kier][i][2] == 0):
                                continue
                            if(tracked_veh[veh_l][veh_b][kier][i][2] > 0):
                                tracked_veh[veh_l][veh_b][kier][i][2] -= 1
                            
                            p_nazwa, p_x, p_y = stops[przystanek[0]][przystanek[1]]
                            p_x, p_y  = float(p_x), float(p_y)
                            
                            veh = vehicles[veh_l][veh_b]
                            
                            odl = ((p_x - veh.location.latitude)**2 + (p_y - veh.location.longitude)**2)**(1/2)
                            if(odl <= limit_odl):
                                #print(f"Bygada {veh.brigade} w okręgu przystanku {p_nazwa} {przystanek[1]}")
                                if (odl < tracked_veh[veh_l][veh_b][kier][i][0]):
                                    print(f"Brygada {veh.brigade} nowe minimum przystanku {p_nazwa} {przystanek[1]} = {odl}")
                                    zapamietaj = 1
                                    tracked_veh[veh_l][veh_b][kier][i][0] = odl
                                    tracked_veh[veh_l][veh_b][kier][i][1] = veh.time
                                    # Dla granicznych przystanków zmniejszamy limit prób! (może tylko jeśli przyjechał na poprzedni... 
                                    # albo wgl nie poprzedni tylko jakiś bardziej z tyłu (bo mogą się nakrywać te dwa końcowe)
                                    if(i == len(przystanki[veh_l][kier]) - 1):
                                        if(tracked_veh[veh_l][veh_b][kier][i-3][2] != -1):
                                            tracked_veh[veh_l][veh_b][kier][i][2] = limit_prob_gr
                                        else:
                                            tracked_veh[veh_l][veh_b][kier][i][2] = limit_prob
                                    else:
                                        tracked_veh[veh_l][veh_b][kier][i][2] = limit_prob
                        
                        statusy[kier] = status
                        if(zapamietaj):
                            print(statusy)
                            print(statusy_cz)
                    # Jeżeli na ostatnich przystankach nie czekamy na nowe minima
                    if(statusy[kierunki[0]] <= 0 and statusy[kierunki[1]] <= 0):
                        
                        if(statusy[kierunki[0]] == 0 and statusy[kierunki[1]] == 0):
                            # Sprawdzamy jaki jest prawdziwy kierunek (na podstawie numeru ostatniego przystanku w daną stronę)
                            if(statusy_cz[kierunki[0]][0] > statusy_cz[kierunki[1]][0]):
                                kier = kierunki[0]
                            elif(statusy_cz[kierunki[0]][0] < statusy_cz[kierunki[1]][0]):
                                kier = kierunki[1]
                            else: # Jeśli było tyle samo to sprawdzamy na podstawie czasu z ostatniego przystanku w daną stronę)   
                                if(statusy_cz[kierunki[0]][1] > statusy_cz[kierunki[1]][1]):
                                    kier = kierunki[0]
                                else:
                                    kier = kierunki[1]
                            print(f"Zapisujemy do pliku brygadę {veh_b}. Prawdziwy kierunek to {kier}")
                            for i, przystanek in enumerate(przystanki[veh_l][kier]):
                                if(tracked_veh[veh_l][veh_b][kier][i][1] != 0):
                                    writer.writerow([stops[przystanek[0]][przystanek[1]][0], przystanek[1], veh_l, kier, str(czas.date()), tracked_veh[veh_l][veh_b][kier][i][1].strftime('%H:%M:%S')])
                            plik.flush()
                            status = -2
                            del tracked_veh[veh_l][veh_b]
                        
                        # Jeśli -1 i 0 to daj mu jakiś czas (np. 15 minut i jeśli to się nie zmieni tzn. że zaczęliśmy go łapać jak był już na ostatnim przystanku)
                        elif(statusy[kierunki[0]] == -1 and statusy[kierunki[1]] == 0): 
                            print(f"Dzwiny przypadek statusowy dla brygady {veh_b}. Czy tak już zostanie?")
                        elif(statusy[kierunki[0]] == 0 and statusy[kierunki[1]] == -1): 
                            print(f"Dzwiny przypadek statusowy dla brygady {veh_b}. Czy tak już zostanie?")
                                            
            #print(tracked_veh)
            #return 0
            
            roznica = datetime.now() - czas
            roznica_s = 10 - roznica.seconds
            if (roznica_s > 0):
                time.sleep(roznica_s)
                    
                
if __name__ == "__main__":
    main()
