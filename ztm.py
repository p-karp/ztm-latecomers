import warsaw_data_api as wawztm
import matplotlib.pyplot as plt
import numpy as np

# Utwórz obiekt API
ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')


'''
# Pobierz ID przystanku "Czarnomorska"
Czarnomorska_id = ztm.get_bus_stop_id_by_bus_stop_name("Czarnomorska")

# Pobierz linie autobusowe dla danego przystanku
lines = ztm.get_lines_for_bus_stop_id(Czarnomorska_id, "01")
print(lines)

# Pobierz harmonogram dla każdej linii
for line in lines:
    print(f"\n\nLinia {line}\n")
    schedule = ztm.get_bus_stop_schedule_by_name("Czarnomorska", "01", line)
    print(schedule.rides)
    for ride in schedule.rides:
        print(ride.time)        # przykładowe odwoływanie się do atrybutu schedule.rides.time
'''

# # przystanki czasprzykład
# schedule = ztm.get_bus_stop_schedule_by_name("Czarnomorska", "52", 501)
# print(schedule.rides[0].time)


# autobusy przykład
exp = True
while(exp):
    try:
        buses = ztm.get_buses_location()
        exp = False
    except TypeError:
        exp = True


# for bus in buses:
#     print(bus)

'''52.186976, 20.996952'''

x = np.zeros(1000, dtype=float)
y = np.zeros(1000, dtype=float)
j = 0
i = 0
while j < 1000:
    print(buses[i].lines)                # numer linii
    print(buses[i].vehicle_number)       # numer autobusu
    print(buses[i].time)        # chyba czas ostatniej aktualizacji pozycji
    print(buses[i].location)    
    print(type(buses[i].location.latitude))
    print(buses[i].location.latitude)   # szerokość geograficzna
    print(type(buses[i].location.longitude))
    print(buses[i].location.longitude)  # długość geograficzna
    
    if(buses[i].location.latitude > 52 and buses[i].location.latitude > 21):
        x[j] = buses[i].location.longitude
        y[j] = buses[i].location.latitude
        j = j + 1
    i = i + 1



trams = ztm.get_trams_location()
x_t = np.zeros(400, dtype=float)
y_t = np.zeros(400, dtype=float)
j = 0
i = 0
while j < 400:
    print(trams[i].lines)                # numer linii
    print(trams[i].vehicle_number)       # numer autobusu
    print(trams[i].time)        # chyba czas ostatniej aktualizacji pozycji
    print(trams[i].location)    
    print(type(trams[i].location.latitude))
    print(trams[i].location.latitude)   # szerokość geograficzna
    print(type(trams[i].location.longitude))
    print(trams[i].location.longitude)  # długość geograficzna
    
    if(trams[i].location.latitude > 52 and trams[i].location.latitude > 21):
        x_t[j] = trams[i].location.longitude
        y_t[j] = trams[i].location.latitude
        j = j + 1
    i = i + 1

plt.scatter(x, y, color = 'hotpink')
plt.scatter(x_t, y_t, color = '#88c999')
# plt.xlim(52,53)
# plt.ylim(20,22)
plt.show()


'''
# przystanki czasprzykład
schedule = ztm.get_bus_stop_schedule_by_name("Czarnomorska", "01", 501)
print(schedule.rides[25].time)
'''