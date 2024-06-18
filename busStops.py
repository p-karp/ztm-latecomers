import requests
import time

def getBusStopsData() -> dict:
    # URL API z kluczem API
    url = 'https://api.um.warszawa.pl/api/action/dbstore_get/?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630&sortBy=id&apikey=7febd25f-aa4e-4c31-8b8a-d517530106ca'
    
    # Wykonaj zapytanie HTTP GET
    exp = True
    while(exp):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                exp = False
            else:
                time.sleep(2)
                return f'Błąd: {response.status_code}'
        except Exception as e:
            time.sleep(5)
            print(f"Zwrócono wyjątek: {e}")
    # Sprawdź, czy zapytanie zakończyło się sukcesem
    D = {}
    result = data["result"]
    for i in range(len(result)):
        if result[i]["values"][0]["value"] not in D.keys(): D[result[i]["values"][0]["value"]] = {}
        D[result[i]["values"][0]["value"]][result[i]["values"][1]["value"]] = (result[i]["values"][2]["value"],
                                                   result[i]["values"][4]["value"], result[i]["values"][5]["value"])
    return D

# Konwersja z formatu od Hani na ID
'''
nazwy = ['pl.Wilsona 05', 'Czarnieckiego 01', 'Centrum Olimpijskie 02', 'most Grota-Roweckiego 02', 'Żerań FSO 04', 'PKP Toruńska 02', 'Bazyliańska 01']

b = getBusStopsData()

do_wyplucia = "["

for n in nazwy:
    na = n[:-3]
    nr = n[-2:]
    
    znaleziono = 0
    
    for x in b.keys():
        if(nr in b[x]):
            if(b[x][nr][0] == na):
                znaleziono = 1
                print(f"{n} --- {x}")
                do_wyplucia += f"('{x}', '{nr}'), "
    if not znaleziono:
        print(f"NIE ZNALEZIONO PRZYSTANKU: {n}")

do_wyplucia = do_wyplucia[:-2]
do_wyplucia += "]"

print(do_wyplucia)    
'''
