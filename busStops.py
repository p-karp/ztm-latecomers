import requests

def getBusStopsData():
    # URL API z kluczem API
    url = 'https://api.um.warszawa.pl/api/action/dbstore_get/?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630&sortBy=id&apikey=7febd25f-aa4e-4c31-8b8a-d517530106ca'

    # Wykonaj zapytanie HTTP GET
    response = requests.get(url)
    # Sprawdź, czy zapytanie zakończyło się sukcesem
    if response.status_code == 200:
        data = response.json()
    else:
        return f'Błąd: {response.status_code}'
    D = {}
    result = data["result"]
    for i in range(len(result)):
        if result[i]["values"][0]["value"] not in D.keys(): D[result[i]["values"][0]["value"]] = []
        D[result[i]["values"][0]["value"]].append((result[i]["values"][1]["value"], result[i]["values"][2]["value"],
                                                   result[i]["values"][4]["value"], result[i]["values"][5]["value"]))
    return D


# print(data["result"][0]["values"][0]["value"]) # id przystanku
# print(data["result"][0]["values"][1]["value"]) # nr przystanku
# print(data["result"][0]["values"][2]["value"]) # nazwa przystanku
# print(data["result"][0]["values"][3]["value"]) # id ulicy
# print(data["result"][0]["values"][4]["value"]) # szer_geo
# print(data["result"][0]["values"][5]["value"]) # dług_geo