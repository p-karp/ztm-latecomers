import warsaw_data_api as wawztm
import time
from datetime import datetime
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed


"""
    Pozyskiwanie rozkładów jazdy po id przystanków.

    INPUT:
        przyjmuje przystanki w formie listy, gdzie argumentem jest np. ("2098", "01", "141").
    
    OUTPUT:
        nic nie zwraca, ale zapisuje pozyskane planowe przyjazdy pojazdów do pliku: "busSchedules.csv"
        w formacie: przystanek;nr_przystanku;linia;dzień;godzina docelowa\n.
    
    LOG:
        kontrolnie wypisuje czas uzyskiwania wszystkich rozkładów jazdy.
"""
def fetch_schedule_by_ids(przystanki):
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
    def fetch_schedule(przystanek):
        while True:
            try:
                schedule = ztm.get_bus_stop_schedule_by_id(przystanek[0], przystanek[1], przystanek[2])
                return przystanek, schedule
            except Exception as e:
                time.sleep(2)
                print(f"Zwrócono wyjątek: {e}")

    # przygotowanie pliku do zapisu
    file_name = f"zebraneDane/rj_{datetime.now().strftime('%d-%m')}.csv"
    kolumny = ["przystanek", "nr_przystanku", "linia", "dzień", "godzina docelowa"]
    date = datetime.now()

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';', lineterminator = "\n")
        writer.writerow(kolumny)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_przystanek = {executor.submit(fetch_schedule, przystanek): przystanek for przystanek in przystanki}
            for future in as_completed(future_to_przystanek):
                przystanek, schedule = future.result()
                for ride in schedule.rides:
                    writer.writerow([przystanek[0], przystanek[1], przystanek[2], str(date.date()), ride.time])

    date1 = datetime.now()
    print("Time spent for fetching schedules by ids:", date1 - date)




"""
    Pozyskiwanie rozkładów jazdy po nazwie przystanku.

    INPUT:
        przyjmuje przystanki w formie listy, gdzie argumentem jest np. ("2098", "01", "141").
    
    OUTPUT:
        nic nie zwraca, ale zapisuje pozyskane planowe przyjazdy pojazdów do pliku: "busSchedules.csv"
        w formacie: przystanek;nr_przystanku;linia;dzień;godzina docelowa\n.
    
    LOG:
        kontrolnie wypisuje czas uzyskiwania wszystkich rozkładów jazdy.
"""
def fetch_schedule_by_names(przystankiNAMES):
    ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
    def fetch_schedule(przystanek):
        while True:
            try:
                schedule = ztm.get_bus_stop_schedule_by_name(przystanek[0], przystanek[1], przystanek[2])
                return przystanek, schedule
            except Exception as e:
                time.sleep(2)
                print(f"Zwrócono wyjątek: {e}")

    # przygotowanie pliku do zapisu
    file_name = "busSchedules.csv"
    kolumny = ["przystanek", "nr_przystanku", "linia", "dzień", "godzina docelowa"]
    date = datetime.now()

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(kolumny)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_przystanek = {executor.submit(fetch_schedule, przystanek): przystanek for przystanek in przystankiNAMES}
            for future in as_completed(future_to_przystanek):
                przystanek, schedule = future.result()
                for ride in schedule.rides:
                    writer.writerow([przystanek[0], przystanek[1], przystanek[2], str(date.date()), ride.time])

    date1 = datetime.now()
    print("Time spent for fetching schedules by names:", date1 - date)


'''Przykładowe testy'''
# p = [
#     ("2098", "01", "141"), ("2098", "01", "143"), ("2098", "01", "182"), ("2098", "01", "188"), ("2098", "01", "523"), ("7009", "01", "520"), ("7009", "01", "525"), ("7009", "01", "514"), ("7009", "01", "502"),
#     ("2098", "02", "141"), ("2098", "02", "143"), ("2098", "02", "182"), ("2098", "02", "188"), ("2098", "02", "523"), ("7009", "02", "520"), ("7009", "02", "525"), ("7009", "02", "514"), ("7009", "02", "502"),
#     ("7009", "01", "182"), ("7009", "01", "143"), ("7009", "01", "138"), ("7009", "01", "187"), ("7009", "01", "523"), ("7009", "01", "520"), ("7009", "01", "525"), ("7009", "01", "514"), ("7009", "01", "502"), ("7009", "01", "411"),
#     ("7009", "02", "182"), ("7009", "02", "143"), ("7009", "02", "138"), ("7009", "02", "187"), ("7009", "02", "523"), ("7009", "02", "520"), ("7009", "02", "525"), ("7009", "02", "514"), ("7009", "02", "502"), ("7009", "02", "411"),
#     ("7041", "05", "7"), ("7041", "05", "9"), ("7041", "05", "22"), ("7041", "05", "24"), ("7041", "05", "25"),
#     ("7041", "06", "7"), ("7041", "06", "9"), ("7041", "06", "22"), ("7041", "06", "24"), ("7041", "06", "25")
# ]


# pN = [
#     ("Międzynarodowa", "01", "141"), ("Międzynarodowa", "01", "143"), ("Międzynarodowa", "01", "182"), ("Międzynarodowa", "01", "188"), ("Międzynarodowa", "01", "523"), ("Marszałkowska", "01", "520"), ("Marszałkowska", "01", "525"), ("Marszałkowska", "01", "514"), ("Marszałkowska", "01", "502"),
#     ("Międzynarodowa", "02", "141"), ("Międzynarodowa", "02", "143"), ("Międzynarodowa", "02", "182"), ("Międzynarodowa", "02", "188"), ("Międzynarodowa", "02", "523"), ("Marszałkowska", "02", "520"), ("Marszałkowska", "02", "525"), ("Marszałkowska", "02", "514"), ("Marszałkowska", "02", "502"),
#     ("Marszałkowska", "01", "182"), ("Marszałkowska", "01", "143"), ("Marszałkowska", "01", "138"), ("Marszałkowska", "01", "187"), ("Marszałkowska", "01", "523"), ("Marszałkowska", "01", "520"), ("Marszałkowska", "01", "525"), ("Marszałkowska", "01", "514"), ("Marszałkowska", "01", "502"), ("Marszałkowska", "01", "411"),
#     ("Marszałkowska", "02", "182"), ("Marszałkowska", "02", "143"), ("Marszałkowska", "02", "138"), ("Marszałkowska", "02", "187"), ("Marszałkowska", "02", "523"), ("Marszałkowska", "02", "520"), ("Marszałkowska", "02", "525"), ("Marszałkowska", "02", "514"), ("Marszałkowska", "02", "502"), ("Marszałkowska", "02", "411"),
#     ("Muzeum Narodowe", "05", "7"), ("Muzeum Narodowe", "05", "9"), ("Muzeum Narodowe", "05", "22"), ("Muzeum Narodowe", "05", "24"), ("Muzeum Narodowe", "05", "25"),
#     ("Muzeum Narodowe", "06", "7"), ("Muzeum Narodowe", "06", "9"), ("Muzeum Narodowe", "06", "22"), ("Muzeum Narodowe", "06", "24"), ("Muzeum Narodowe", "06", "25")
# ]



# fetch_schedule_by_ids(p)
# time.sleep(3)
# fetch_schedule_by_names(pN)