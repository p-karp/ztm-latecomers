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
    limit_prob = 6*10 # 15 minut TODO: zrobić większe potem
    
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
                    kierunki = list(przystanki[veh_l].keys())
                    if veh_b not in tracked_veh[veh_l]:
                        tracked_veh[veh_l][veh_b] = [0, {kierunki[0]: [[1000, 0, -1] for _ in przystanki[veh_l][kierunki[0]]], kierunki[1]: [[1000, 0, -1] for _ in przystanki[veh_l][kierunki[1]]]}]
                    statusy = {kierunki[0]:-2,kierunki[1]: -2}
                    for kier in tracked_veh[veh_l][veh_b][1]:
                        if(tracked_veh[veh_l][veh_b][0] != 0):
                            if(tracked_veh[veh_l][veh_b][0] != kier):
                                continue
                        status = -1
                        for i, przystanek in enumerate(przystanki[veh_l][kier]):
                            status = max(status, tracked_veh[veh_l][veh_b][1][kier][i][2])
                            if(tracked_veh[veh_l][veh_b][1][kier][i][2] == 0):
                                continue
                            tracked_veh[veh_l][veh_b][1][kier][i][2] -= 1
                            
                            p_nazwa, p_x, p_y = stops[przystanek[0]][przystanek[1]]
                            p_x, p_y  = float(p_x), float(p_y)
                            
                            veh = vehicles[veh_l][veh_b]
                            
                            odl = ((p_x - veh.location.latitude)**2 + (p_y - veh.location.longitude)**2)**(1/2)
                            if(odl <= limit_odl):
                                #print(f"Bygada {veh.brigade} w okręgu przystanku {p_nazwa} {przystanek[1]}")
                                if (odl < tracked_veh[veh_l][veh_b][1][kier][i][0]):
                                    print(f"Bygada {veh.brigade} nowe minimum przystanku {p_nazwa} {przystanek[1]} = {odl}")
                                    tracked_veh[veh_l][veh_b][1][kier][i][0] = odl
                                    tracked_veh[veh_l][veh_b][1][kier][i][1] = veh.time
                                    tracked_veh[veh_l][veh_b][1][kier][i][2] = limit_prob
                                    if(tracked_veh[veh_l][veh_b][0] == 0):
                                        if(i > 0):
                                            if(tracked_veh[veh_l][veh_b][1][kier][i-1][1] != 0):
                                                if(tracked_veh[veh_l][veh_b][1][kier][i-1][1] < tracked_veh[veh_l][veh_b][1][kier][i][1]):
                                                    print(f"Określono prawidlowy kierunek! {kier}")
                                                    tracked_veh[veh_l][veh_b][0] = kier
                        
                        statusy[kier] = status
                        if(status == 0):
                            if(tracked_veh[veh_l][veh_b][0] == 0):
                                if(tracked_veh[veh_l][veh_b][1][kier][len(przystanki[veh_l][kier])-1][2] == 0):
                                    print(f"Określono prawidlowy kierunek (przypadek graniczny)! {kier}")
                                    tracked_veh[veh_l][veh_b][0] = kier
                            else:
                                print(f"Zapisujemy do pliku brygadę {veh_b}")
                                for i, przystanek in enumerate(przystanki[veh_l][kier]):
                                    writer.writerow([stops[przystanek[0]][przystanek[1]][0], przystanek[1], veh_l, kier, str(czas.date()), tracked_veh[veh_l][veh_b][1][kier][i][1]].strftime('%H:%M:%S'))
                                plik.flush()
                                status = -2
                                del tracked_veh[veh_l][veh_b]
                                break
                    if(statusy[kierunki[0]] == 0 and statusy[kierunki[1]] == 0):
                        print("To znaczy że był jakiś solidny błąd!")
                        # Tutaj resetujemy listę dla danej brygady i zapisujemy błąd (aktualny stan) do pliku
                                            
            #print(tracked_veh)
            #return 0
            
            roznica = datetime.now() - czas
            roznica_s = 10 - roznica.seconds
            if (roznica_s > 0):
                time.sleep(roznica_s)
                    
                
if __name__ == "__main__":
    main()
