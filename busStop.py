import busStops
import warsaw_data_api as wawztm

D = busStops.getBusStopsData()
ztm = wawztm.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')

# wygodna klasa BusStop
class BusStop:
    def __init__(self, id, nr):
        self.id = id
        self.name = D[id][1]
        self.nr = nr
        for el in D[id]:
            if(el[0] == nr): 
                self.x, self.y = el[2], el[3]

    def __str__(self):
        return f"BusStop(id:{self.id} nazwa:{self.name} nr:{self.nr} szer:{self.x} dł:{self.y})"

# def getSchedule(id,nr,line):
#     tab = []
#     schedule = ztm.get_bus_stop_schedule_by_id(id, nr, line)
#     for rec in schedule.rides:
#         tab.append(rec.time)
#     return tab

def getBS(busStopsNames, busStopsNr):
    BS = []
    for i,busStop in enumerate(busStopsNames):
        BS.append(BusStop(ztm.get_bus_stop_id_by_bus_stop_name(busStop), busStopsNr[i]))
    return BS

print(getBS(["Ochota-Ratusz", "pl.Narutowicza", "Wawelska"], ["02", "08", "04"])[0])