import processing as pr
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# Funkcja obliczająca średnie opóźnienie przystanków
def oblicz_opoznienie(czas_przyjazdu, czas_rozkład):
    lista_opoznien = []
    
    for rozklad in czas_rozkład:
        lista_roznic = []
        for przyjazd in czas_przyjazdu:
            roznica_czasu = datetime.strptime(przyjazd, '%H:%M:%S') - datetime.strptime(rozklad, '%H:%M:%S')
            roznica_minuty = roznica_czasu.total_seconds() / 60.0
            lista_roznic.append(np.abs(roznica_minuty))
        
        minimalna_roznica = np.min(lista_roznic)
        lista_opoznien.append(minimalna_roznica)
    
    srednie_opoznienie = np.mean(lista_opoznien)
    return srednie_opoznienie

# Funkcja przetwarzająca dane dla przystanków, dni, linii i mostów
def przetwarzanie_danych(przyjazdy, rozklady, funkcja_kluczowania):
    dane_przystanki = {}
    
    for linia in przyjazdy.keys():
        for przystanek in przyjazdy[linia].keys():
            for numer in przyjazdy[linia][przystanek].keys():
                for data in przyjazdy[linia][przystanek][numer].keys():
                    klucz = funkcja_kluczowania(linia, przystanek, numer, data)
                    
                    czas_przyjazdu = przyjazdy[linia][przystanek][numer][data]
                    czas_rozkład = rozklady[linia][przystanek][numer][data]
                    
                    opoznienie = oblicz_opoznienie(czas_przyjazdu, czas_rozkład)
                    
                    dane_przystanki[klucz] = opoznienie
    
    return dane_przystanki


def klucz_przystanek(linia, przystanek, numer, data):
    return f"{przystanek} {numer}"

def klucz_dzień(linia, przystanek, numer, data):
    return data

def klucz_linia(linia, przystanek, numer, data):
    return str(linia)

def klucz_most(linia, przystanek, numer, data):
    mosty = {
        114: 'most Grota - Roweckiego',
        500: 'most Gdański', 6: 'most Gdański',
        190: 'most Śląsko - Dąbrowski', 26: 'most Śląsko - Dąbrowski',
        162: 'most Świętokrzyski',
        9: 'most Poniatowskiego', 521: 'most Poniatowskiego',
        523: 'most Łazienkowski',
        148: 'most Siekierkowski'
    }
    return mosty.get(linia, 'Inny most')


# Funkcja tworząca wykresy
def wykres(argumenty, wartosci, nazwa_x, nazwa_y, tytul):
    plt.figure(figsize=(30, 7))
    plt.bar(argumenty, wartosci, color='skyblue')
    plt.xlabel(nazwa_x)
    plt.ylabel(nazwa_y)
    plt.xticks(rotation='vertical')
    plt.title(tytul)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


# Funkcja obliczająca opóźnienia w zależności od pory dnia
def opoznienia_pory(przyjazdy, rozklady):
    pory_dnia = {
        'ranek': [],
        'przedpołudnie': [],
        'popołudnie': [],
        'wieczór': [],
        'noc': []
    }

    for linia in przyjazdy.keys():
        for przystanek in przyjazdy[linia].keys():
            for numer in przyjazdy[linia][przystanek].keys():
                for data in przyjazdy[linia][przystanek][numer].keys():
                    czas_przyjazdu = przyjazdy[linia][przystanek][numer][data]
                    czas_rozkład = rozklady[linia][przystanek][numer][data]
                    
                    for przyjazd in czas_przyjazdu:
                        min_opoznienie_dla_przyjazdu = np.inf  # inicjalizacja jako nieskończoność
                        
                        for rozklad in czas_rozkład:
                            czas_przyjazdu_dt = datetime.strptime(przyjazd, '%H:%M:%S')
                            czas_rozkład_dt = datetime.strptime(rozklad, '%H:%M:%S')
                            roznica_czasu = np.abs((czas_przyjazdu_dt - czas_rozkład_dt).total_seconds() / 60.0)
                            
                            if roznica_czasu < min_opoznienie_dla_przyjazdu:
                                min_opoznienie_dla_przyjazdu = roznica_czasu
                        
                        # Przypisanie minimalnego opóźnienia do odpowiedniego przedziału czasowego
                        if 0 <= czas_przyjazdu_dt.hour < 9:
                            pory_dnia['ranek'].append(min_opoznienie_dla_przyjazdu)
                        elif 9 <= czas_przyjazdu_dt.hour < 12:
                            pory_dnia['przedpołudnie'].append(min_opoznienie_dla_przyjazdu)
                        elif 12 <= czas_przyjazdu_dt.hour < 16:
                            pory_dnia['popołudnie'].append(min_opoznienie_dla_przyjazdu)
                        elif 16 <= czas_przyjazdu_dt.hour < 20:
                            pory_dnia['wieczór'].append(min_opoznienie_dla_przyjazdu)
                        else:
                            pory_dnia['noc'].append(min_opoznienie_dla_przyjazdu)
    
    # Obliczenie średnich opóźnień dla poszczególnych przedziałów czasowych
    opoznienia_pory= {}
    for pora, opoznienia in pory_dnia.items():
        if opoznienia:
            opoznienia_pory[pora] = np.mean(opoznienia)

    
    return opoznienia_pory


nazwy_plikow = [
    ('./zebraneDane/dane_ok/rj_29-06.csv', './zebraneDane/dane_ok/dane_29-06.csv'),
    ('./zebraneDane/dane_ok/rj_30-06.csv', './zebraneDane/dane_ok/dane_30-06.csv'),
    ('./zebraneDane/dane_ok/rj_01-07.csv', './zebraneDane/dane_ok/dane_01-07.csv'),
    ('./zebraneDane/dane_ok/rj_02-07.csv', './zebraneDane/dane_ok/dane_02-07.csv'),
    ('./zebraneDane/dane_ok/rj_04-07.csv', './zebraneDane/dane_ok/dane_04-07.csv'),
    ('./zebraneDane/dane_ok/rj_05-07.csv', './zebraneDane/dane_ok/dane_05-07.csv')
]

# Przetwarzanie danych i tworzenie wykresów dla każdego pliku
for plik_przyjazd, plik_rozkład in nazwy_plikow:
    dane_przyjazd, dane_rozkład = pr.processing(plik_przyjazd, plik_rozkład)
    
    dane_przystanki = przetwarzanie_danych(dane_przyjazd, dane_rozkład, klucz_przystanek)
    dane_dni = przetwarzanie_danych(dane_przyjazd, dane_rozkład, klucz_dzień)
    dane_linia = przetwarzanie_danych(dane_przyjazd, dane_rozkład, klucz_linia)
    dane_mosty = przetwarzanie_danych(dane_przyjazd, dane_rozkład, klucz_most)
    opoznienia_pory_dnia = oblicz_opoznienie_pory_dnia(dane_przyjazd, dane_rozkład)

    # Tworzenie wykresów
    wykres(list(dane_przystanki.keys()), list(dane_przystanki.values()), 'Przystanki', 'Opóźnienie [min]', f'Opóźnienia dla danych przystanków w dniu {plik_przyjazd}')
    wykres(list(dane_dni.keys()), list(dane_dni.values()), 'Data', 'Opóźnienie [min]', f'Opóźnienia w dniu {plik_przyjazd}')
    wykres(list(dane_linia.keys()), list(dane_linia.values()), 'Numery Linii', 'Opóźnienie [min]', f'Opóźnienia dla danej linii w dniu {plik_przyjazd}')
    wykres(list(dane_mosty.keys()), list(dane_mosty.values()), 'Nazwa mostu', 'Opóźnienie [min]', f'Opóźnienia dla danego mostu w dniu {plik_przyjazd}')
    wy