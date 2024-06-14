import warsaw_data_api

ztm = warsaw_data_api.ztm(apikey='7febd25f-aa4e-4c31-8b8a-d517530106ca')
#schedule = ztm.get_bus_stop_schedule_by_name("Marszałkowska", "01", "182")
#lines = ztm.get_lines_for_bus_stop_id("7002", "01")

bus = ztm.get_buses_location(line="N01", brigade="5")
for b in bus:
    print(b.brigade)

#print(schedule.rides)
