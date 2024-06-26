import warsaw_data_api as wawztm
import busStops as bs

ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
# Pobierz ID przystanku
id = ztm.get_bus_stop_id_by_bus_stop_name("Czarnomorska")

# Pobierz linie autobusowe dla danego przystanku
lines = ztm.get_lines_for_bus_stop_id("3032", "52")
x = bs.getBusStopsData()

print(x[id])
print("id przystanku: ", id)
print("linie: ", lines)


# Pl.Konstytucji 02 01
# Dolna 52 01
# Czarnomorska 52 01
# Nałęczowska 52 51
# Wilanów 02 01
# Czekoladowa 02 01


busS = ['Pl.Konstytucji', 'Dolna', 'Czarnomorska', 'Nałęczowska', 'Wilanów', 'Czekoladowa']
for b in busS:
    id = ztm.get_bus_stop_id_by_bus_stop_name(b)
    print(id, " ", b)