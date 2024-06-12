import warsaw_data_api as wawztm
import busStops as bs

ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
# Pobierz ID przystanku
id = ztm.get_bus_stop_id_by_bus_stop_name("Dwernickiego")

# Pobierz linie autobusowe dla danego przystanku
lines = ztm.get_lines_for_bus_stop_id(id, "01")
x = bs.getBusStopsData()

print(x[id])
print("id przystanku: ", id)
print("linie: ", lines)