import warsaw_data_api as wawztm
import time
import busStops as bs
from datetime import datetime
import csv

# Funkcja pobierające dane o autobusach
def collectBusesData(ztm, linia):
    exp = True
    while(exp):
        try:
            buses = ztm.get_buses_location(line = linia)
            exp = False
        except Exception as e:
            time.sleep(2)
            print(f"Zwrócono wyjątek: {e}")
    return buses


# Funkcja pobierające dane o tramwajach
def collectTramsData(ztm, linia):
    exp = True
    while(exp):
        try:
            trams = ztm.get_trams_location(line = linia)
            exp = False
        except Exception as e:
            time.sleep(2)
            print(f"Zwrócono wyjątek: {e}")
    return trams
 
# Funkcja pobierające dane o rozkładach jazdy   
def collectScheduleData(ztm, przystanek):
    exp = True
    while(exp):
        try:
            schedule = ztm.get_bus_stop_schedule_by_id(przystanek[0], przystanek[1], przystanek[2])
            exp = False
        except Exception as e:
            time.sleep(2)
            print(f"Zwrócono wyjątek: {e}")
    return schedule

'''
Tutaj określamy które przystanki i linie bierzemy pod uwagę
'''
# Autobusy: Szaserów-Szpital, Marszałkowska, Międzynarodowa, Dw.Zachodni, Konarskiego, Roschata, Nałęczowska, Czarnomorska, Dolna, Pl.Konstytucji
# Tramwaje: Hynka, Wawelska, Muzeum Narodowe, Wiatraczna

przystanki = [
              ("2112", "02", "102"), ("2112", "02", "188"), ("2112", "02", "202"), ("2112", "02", "523"),
              ("2112", "01", "102"), ("2112", "01", "188"), ("2112", "01", "202"), ("2112", "01", "523"),
              ("2098", "01", "141"), ("2098", "01", "143"), ("2098", "01", "182"), ("2098", "01", "188"), ("2098", "01", "523"), ("7009", "01", "520"), ("7009", "01", "525"), ("7009", "01", "514"), ("7009", "01", "502"),
              ("2098", "02", "141"), ("2098", "02", "143"), ("2098", "02", "182"), ("2098", "02", "188"), ("2098", "02", "523"), ("7009", "02", "520"), ("7009", "02", "525"), ("7009", "02", "514"), ("7009", "02", "502"),
              ("7009", "01", "182"), ("7009", "01", "143"), ("7009", "01", "138"), ("7009", "01", "187"), ("7009", "01", "523"), ("7009", "01", "520"), ("7009", "01", "525"), ("7009", "01", "514"), ("7009", "01", "502"), ("7009", "01", "411"),
              ("7009", "02", "182"), ("7009", "02", "143"), ("7009", "02", "138"), ("7009", "02", "187"), ("7009", "02", "523"), ("7009", "02", "520"), ("7009", "02", "525"), ("7009", "02", "514"), ("7009", "02", "502"), ("7009", "02", "411"),
              ("4044", "02", "182"), ("7009", "02", "517"), ("7009", "02", "187"), ("7009", "02", "523"), ("4044", "02", "172"), ("7009", "02", "159"), ("7009", "02", "158"), ("7009", "02", "127"),
              ("4044", "01", "182"), ("7009", "01", "517"), ("7009", "01", "187"), ("7009", "01", "523"), ("4044", "01", "172"), ("7009", "01", "159"), ("7009", "01", "158"), ("7009", "01", "127"),
              ("7009", "01", "167"), ("7009", "01", "171"), ("7009", "01", "190"), ("7009", "01", "249"), ("5033", "01", "523"),
              ("7009", "02", "167"), ("7009", "02", "171"), ("7009", "02", "190"), ("7009", "01", "249"), ("5033", "02", "523"),

              ("3048", "02", "139"), ("3048", "02", "251"), ("3048", "02", "339"), ("3048", "02", "519"),
              ("3048", "01", "139"), ("3048", "01", "251"), ("3048", "01", "339"), ("3048", "01", "519"),
              ("3044", "01", "139"), ("3044", "01", "164"), ("3044", "01", "200"), ("3044", "01", "251"), ("3044", "01", "339"), ("3044", "01", "519"),
              ("3044", "02", "139"), ("3044", "02", "164"), ("3044", "02", "200"), ("3044", "02", "251"), ("3044", "02", "339"), ("3044", "02", "519"),
              ("3035", "52", "116"), ("3035", "52", "519"), ("3035", "52", "522"), ("3035", "52", "E-2"),
              ("3035", "01", "116"), ("3035", "01", "519"), ("3035", "01", "522"), ("3035", "01", "E-2"),
              ("3032", "52", "116"), ("3032", "52", "519"), ("3032", "52", "522"), ("3032", "52", "E-2"),
              ("3032", "01", "116"), ("3032", "01", "519"), ("3032", "01", "522"), ("3032", "01", "E-2"),
              ("3027", "52", "116"), ("3027", "52", "166"), ("3027", "52", "503"), ("3027", "52", "519"), ("3027", "52", "522"),("3027", "52", "E-2"),
              ("3027", "01", "116"), ("3027", "01", "166"), ("3027", "01", "503"), ("3027", "01", "519"), ("3027", "01", "522"),("3027", "01", "E-2"),
              ("7011", "02", "131"), ("7011", "02", "519"), ("7011", "02", "522"), ("7011", "02", "525"),
              ("7011", "01", "131"), ("7011", "01", "519"), ("7011", "01", "522"), ("7011", "01", "525"),

              ("4011", "03", "9"), ("4011", "03", "7"),
              ("4011", "04", "9"), ("4011", "04", "7"),
              ("4121", "03", "1"), ("4121", "03", "7"), ("4121", "03", "9"), ("4121", "03", "25"),
              ("4121", "04", "1"), ("4121", "04", "7"), ("4121", "04", "9"), ("4121", "04", "25"),
              ("7041", "05", "7"), ("7041", "05", "9"), ("7041", "05", "22"), ("7041", "05", "24"), ("7041", "05", "25"),
              ("7041", "06", "7"), ("7041", "06", "9"), ("7041", "06", "22"), ("7041", "06", "24"), ("7041", "06", "25"),
              ("2008", "07", "9"), ("2008", "07", "24"),
              ("2008", "06", "9"), ("2008", "06", "24"),
              ]
# TODO: pododawać więcej tramwajów, bo dobrze działają

# wersja nocna
# przystanki = [("3032", "01", "N31"), ("3032", "01", "N81")]

# wersja testowa
# przystanki = [
#               ("2098", "01", "141"), ("2098", "01", "143"), ("2098", "01", "182"), ("2098", "01", "188"), ("2098", "01", "523"), ("7009", "01", "520"), ("7009", "01", "525"), ("7009", "01", "514"), ("7009", "01", "502"),
#               ("2098", "02", "141"), ("2098", "02", "143"), ("2098", "02", "182"), ("2098", "02", "188"), ("2098", "02", "523"), ("7009", "02", "520"), ("7009", "02", "525"), ("7009", "02", "514"), ("7009", "02", "502"),
#               ("7009", "01", "182"), ("7009", "01", "143"), ("7009", "01", "138"), ("7009", "01", "187"), ("7009", "01", "523"), ("7009", "01", "520"), ("7009", "01", "525"), ("7009", "01", "514"), ("7009", "01", "502"), ("7009", "01", "411"),
#               ("7009", "02", "182"), ("7009", "02", "143"), ("7009", "02", "138"), ("7009", "02", "187"), ("7009", "02", "523"), ("7009", "02", "520"), ("7009", "02", "525"), ("7009", "02", "514"), ("7009", "02", "502"), ("7009", "02", "411"),
#               ("7041", "05", "7"), ("7041", "05", "9"), ("7041", "05", "22"), ("7041", "05", "24"), ("7041", "05", "25"),
#               ("7041", "06", "7"), ("7041", "06", "9"), ("7041", "06", "22"), ("7041", "06", "24"), ("7041", "06", "25"),
#             ]


''' 
Struktura opoznienia

opoznienia = {"id_przystanku" : {"kierunek": {"nr_linii": {"nr_brygady" : {"godzina_odjazdu": ["min_odl", "czas_przyjazdu" ,"pozostale_proby"]}}}}}
'''

def main():
    # Tworzenie obiektu API
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')

    # Funkcja pobierająca dane o przystankach
    stops = bs.getBusStopsData()
    
    # Pobieranie rozkładów jazdy
    # TODO: To trzeba będzie robić każdego dnia na nowo (bo zmiany w weekend)
    
    czas = datetime.now()
    czas_str = czas.strftime('%H:%M:%S')

    opoznienia = {}
    for przystanek in przystanki:
        schedule = collectScheduleData(ztm, przystanek)
        brygady = {}
        for ride in schedule.rides:
            if ride.time <= czas_str:
                continue
            czas_przyjazdu = ride.time
            if int(czas_przyjazdu[:2]) >= 24:
                            czas_przyjazdu = f"{int(czas_przyjazdu[:2])-24}{czas_przyjazdu[2:]}"
            if ride.brigade not in brygady:
                brygady[ride.brigade] = {czas_przyjazdu : [1000000, 0, 360]} # 1,5 h
            else:
                brygady[ride.brigade][czas_przyjazdu] = [1000000, 0, 360]
        
        if przystanek[0] not in opoznienia:
            opoznienia[przystanek[0]] = {przystanek[1] : {przystanek[2] : brygady}}
        else:
            if przystanek[1] not in opoznienia[przystanek[0]]:
                opoznienia[przystanek[0]][przystanek[1]] = {przystanek[2] : brygady}
            else:
                opoznienia[przystanek[0]][przystanek[1]][przystanek[2]] = brygady
    #print(opoznienia)
    # startowy (aktualny) czas zbierania danych w sekundach
    t = 0
    # limit czasu zbierania danych w sekundach
    t_lim = 7*24*60*60
    # krok czasowy co ile są zbierane dane w sekundach
    dt = 15
    
    # promień okręgu (w stopniach), kiedy jest łapany autobus
    limit_odl = 0.013
    # liczba prób na znalezienie nowego minimum
    limit_prob = 20  # 5 minut TODO: 60 # 15 minut
    
    # Do zapisu w csv
    kolumny = ["przystanek", "nr_przystanku", "linia", "dzień", "godzina docelowa", "godzina faktyczna"]
    nazwa_pliku = "test.csv"
    
    # główna pętla
    with open(nazwa_pliku, mode = 'w', newline = '') as plik:
        writer = csv.writer(plik, delimiter = ';')
        
        writer.writerow(kolumny)
        while(t <= t_lim):
            
            czas = datetime.now()
            czas_str = czas.strftime('%H:%M:%S')
            
            print(f"+-----------------------+")
            print(f"-------{czas_str}----------")
            
            # vehicles = collectBusesData(ztm)
            #TODO: vehicles w pętli iterować po liniach
            # for bus in buses:
            #     print(bus.lines)
            #     print(bus.brigade)
            # {'517': {'1': veh, '2': veh} }

            for przystanek in opoznienia:
                for nr_przystanku in opoznienia[przystanek]:
                    p_nazwa, p_x, p_y = stops[przystanek][nr_przystanku]
                    p_x, p_y  = float(p_x), float(p_y)
                    #print("PRZYSTANEK: " + p_nazwa)
                    for linia in opoznienia[przystanek][nr_przystanku]:
                        #print("LINIA: " + linia)
                        if(len(linia) == 3):
                            vehicles = collectBusesData(ztm, linia)
                        else: 
                            vehicles = collectTramsData(ztm, linia)
                        for brygada in opoznienia[przystanek][nr_przystanku][linia]:
                            if(len(opoznienia[przystanek][nr_przystanku][linia][brygada]) == 0):
                                continue
                            godz_planowa = list(opoznienia[przystanek][nr_przystanku][linia][brygada].keys())[0]
                            godz_planowa_t = datetime.strptime(godz_planowa, '%H:%M:%S')
                            #print("PLANOWY PRZYJAZD: ", godz_planowa)
                            # Trzeba mieć na uwadze że raczej nie może przyjechać za wcześnie (do 10 minut przed czasem)
                            if (godz_planowa_t.hour <= 2 and czas.hour > 10):
                                if ((godz_planowa_t.hour+24)*60 + godz_planowa_t.minute) - (czas.hour*60 + czas.minute) > 10:
                                    continue
                            if (godz_planowa_t.hour*60 + godz_planowa_t.minute) - (czas.hour*60 + czas.minute) > 10:
                                continue
                            opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][2] -= 1 # Zmniejszamy liczbę prób na zmniejszenie minimum
                            print(f"PRZYSTANEK: {p_nazwa} | LINIA: {linia} | ETA: {godz_planowa}")
                            for b in vehicles:          # TODO: Nie trzeba będzie robić już tej pętli bo znamy ją w słowoniku ( ale sprawdzić czy istnieje w słowniku)
                                if (datetime.now().hour*60 + datetime.now().minute) - (b.time.hour*60 + b.time.minute) > 3:
                                    continue 
                                if(b.brigade == brygada):
                                    odl = ((p_x - b.location.latitude)**2 + (p_y - b.location.longitude)**2)**(1/2)
                                    print("Odległość: " + str(odl) + ", Pozotało prób: " + str(opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][2]))
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
                                            writer.writerow([p_nazwa, nr_przystanku, linia, str(czas.date()), godz_planowa, "nie zarejestrowano przyjazdu"])
                                        else:
                                            writer.writerow([p_nazwa, nr_przystanku, linia, str(czas.date()), godz_planowa, opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa][1].strftime('%H:%M:%S')])
                                        plik.flush()
                                        del opoznienia[przystanek][nr_przystanku][linia][brygada][godz_planowa]
                                    break
            roznica = datetime.now() - czas
            roznica_s = 15 - roznica.seconds
            if (roznica_s > 0):
                time.sleep(roznica_s)
            t = t + dt
        

if __name__ == "__main__":
    main()
