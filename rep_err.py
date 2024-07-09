import warsaw_data_api as wawztm
import busStops as bs

ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
# Pobierz ID przystanku
# id = ztm.get_bus_stop_id_by_bus_stop_name("KS Polonia")

# Pobierz linie autobusowe dla danego przystanku
lines = ztm.get_lines_for_bus_stop_id("7053", "02")
x = bs.getBusStopsData()

# print(x[id])
# print("id przystanku: ", id)
# print("linie: ", lines)


nazwy = []
for i in range(1000, 9999):
    id = str(i)
    try:
        name = x[id][list(x[id].keys())[0]][0]
        nazwy.append(name)
        if name == "pl.Na Rozdrożu":
            print(name)
            print(x[id])
            print("id przystanku: ", id)
    except:
        continue

# print(sorted(nazwy))