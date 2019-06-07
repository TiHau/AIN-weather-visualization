import matplotlib.dates as dat
import matplotlib.pyplot as plt
import numpy as np
import grib2_extractor as grb
import FlightData as Fd
import datetime as dt
import geocalc
import time

# arrival_time: time of arrival as last value on x-axis
# height: highest displayed point above sea level
def plotting():

    FEET_TO_METERS = 0.305
    UPPER_LIMIT = 1000
    LOWER_LIMIT = 50

    # NEEDED FOR VISUALIZATION
    # altitude (y-axis)
    # flight time (x axis)
    # wind speed
    # wind direction
    # elevation (separate plot)

    flight_data = Fd.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')

    # Getting the needed values inside a list: Altitude, flight time, angle and speed
    #list_angle = []
    #list_speed = []
    #list_time = []
    #list_alt = []
    #for i in flight_data.entry_list.values():
        #list_angle.append(i.wind_angle)
        #list_speed.append(i.wind_speed)
        #list_time.append(i.time_stamp)
       # list_alt.append(i.attitude)

    #print(str(len(list_angle)), str(len(list_speed)), str(len(list_time)), str(len(list_alt)))
# calculate u and v values (needed for barb plotting)
    #list_u = []
    #list_v = []
    #index_angle = 0
    #cnt = 0
    #for j in list_speed:
       # if cnt > 74:  # ensure that the arrays have a length of 12 FOR TESTING PURPOSE
         #   list_u.append(j * np.cos(list_angle[index_angle]))
        #    list_v.append(j * np.sin(list_angle[index_angle]))
       #     index_angle += 1
      #      cnt = 0
     #   cnt += 1

    #print(list_time)
    #y = np.linspace(0, 60000, 12)
    #x = np.linspace(0, len(list_time), 12)
    # calculate the points on the grid where the wind barbs are to be displayed later
    #xx, yy = np.meshgrid(x, y)

    #cnt = 0
    #xlist = []
    #ylist = []
    #for k in flight_data.entry_list.values():
    #    if cnt > 150:
    #        xlist.append(k.longitude)
    #        ylist.append(k.latitude)
    #        cnt = 0
    #    cnt += 1
    #for k in list_alt:
    #    if cnt > 150:
    #        ylist.append(k)
    #        cnt = 0
    #    cnt += 1

    #for l in list_time:
    #    if cnt > 150:
    #        xlist.append(l)
    #        cnt = 0
    #    cnt += 1

    #dates = dat.date2num(list_time)
    #print(len(list_speed))
    #print(len(list_alt))
    #print(len(listU))
    #print(len(xlist))
    #print(xlist)
    #print(listU)
    #print(len(listU))

    #extracting json data
    grib_data = grb.import_from_json("gfs.t00z.pgrb2.0p25.f003.json")

    res = []
    at_waypoint = []
    for entry in flight_data.get_path_filtered(10):
        tl_lat = geocalc.round_to_nearest_quarter_up(entry.latitude)
        tl_long = geocalc.round_to_nearest_quarter_down(entry.longitude)
        bl_lat = geocalc.round_to_nearest_quarter_down(entry.latitude)
        bl_long = tl_long
        tr_lat = tl_lat
        tr_long = geocalc.round_to_nearest_quarter_up(entry.longitude)
        br_lat = bl_lat
        br_long = tr_long
        tl_grib_values = grib_data[(tl_lat, tl_long)]
        bl_grib_values = grib_data[(bl_lat, bl_long)]
        tr_grib_values = grib_data[(tr_lat, tr_long)]
        br_grib_values = grib_data[(br_lat, br_long)]
        at_waypoint.append(entry)
        res_values = []
        for level in tl_grib_values.values():
            for tl_param in level.parameters.values():
                bl_param = bl_grib_values[level.level].parameters[tl_param.name]
                tr_param = tr_grib_values[level.level].parameters[tl_param.name]
                br_param = br_grib_values[level.level].parameters[tl_param.name]
                try:
                    ip = geocalc.get_interpolated_value(tl_lat, tl_long, tl_param.data, tr_lat, tr_long, tr_param.data,
                                                        bl_lat, bl_long, bl_param.data, br_lat, br_long, br_param.data,
                                                        entry.latitude, entry.longitude)
                    res_values.append((level.level, level.name, tl_param.name, tl_param.unit, ip))
                except:
                    pass
        res.append(res_values)

        # putting data in lists
        heights = {}
        u_comp = {}
        v_comp = {}
        temperature = {}

        for en in res:
            for val in en:
                if LOWER_LIMIT <= val[0] <= UPPER_LIMIT and val[1] == 'isobaricInhPa':
                    if val[2] == 'Geopotential Height':
                        if val[0] not in heights:
                            heights[val[0]] = []
                        heights[val[0]].append(val[4])
                    elif val[2] == 'U component of wind':
                        if val[0] not in u_comp:
                            u_comp[val[0]] = []
                        u_comp[val[0]].append(val[4])
                    elif val[2] == 'V component of wind':
                        if val[0] not in v_comp:
                            v_comp[val[0]] = []
                        v_comp[val[0]].append(val[4])
                    elif val[2] == 'Temperature':
                        if val[0] not in temperature:
                            temperature[val[0]] = []
                        temperature[val[0]].append(val[4])
    print(at_waypoint)
    fig, ax = plt.subplots()

    # plot altitude depending on time
    #new_time = []
    maximum = 0
    #for t in list_time:
     #   new_time.append(dt.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f'))

    lvl_cnt = 0
    for lvl in u_comp.keys():
        lvl_cnt += 1
        #plt.subplot(26, 1, lvl_cnt)
        plt.barbs(np.arange(1, 11), lvl, np.array(u_comp.get(lvl)), np.array(v_comp.get(lvl)),length=5.5 ,rasterized=True)
        if maximum <= int(lvl):
            maximum = int(lvl)

    # Höhe der Wegpunkte
    height_pressure_upper = {}
    height_pressure_lower = {}
    height_pressure_invalid = {}

    #print(len(list(heights.values())[0]))

    index = 0
    lat_lon = []

    for entry in at_waypoint:
        print(entry.attitude*FEET_TO_METERS)
        lat_lon.append(str(entry.latitude) + ",\n " + str(entry.longitude))
        height_pressure_upper[index+1] = []
        height_pressure_lower[index+1] = []
        height_pressure_invalid[index+1] = []
        for (k,v) in heights.items():
            #print(str(entry.attitude) + " : ")
            if v[index] > entry.attitude*FEET_TO_METERS:
                height_pressure_upper[index+1].append(k)
            if v[index] < entry.attitude*FEET_TO_METERS:
                height_pressure_lower[index+1].append(k)
            if v[index] == entry.attitude*FEET_TO_METERS:
                height_pressure_invalid[index + 1].append(k)
        index += 1

    print(lat_lon)

    pressure_upper = []
    for entry in height_pressure_upper.values():
        try:
            pressure_upper.append(entry[len(entry)-1])
        except IndexError:
            pass

    pressure_lower = []
    for entry in height_pressure_lower.values():
        try:
            pressure_lower.append(entry[0])
        except IndexError:
            pressure_lower.append(float(UPPER_LIMIT))

    # plot barb for each grid coordinate
    #plt.barbs(new_time, pressure[0], np.array(u_comp), np.array(v_comp))

    #ticks = np.linspace(0, l)
    #plt.yticks(u_comp.keys())
    # Flughöhe in Metern anzeigen

    #ax.plot(new_time, list_alt)
    #plt.gcf().autofmt_xdate()
    plt.grid()
    plt.plot(np.arange(1,11, step=1), pressure_upper)
    plt.plot(np.arange(1,11, step=1), pressure_lower)
    ax.set_xlabel("Waypoints")
    ax.set_xticks(np.arange(1,11, step=1))
    ax.set_xticklabels(lat_lon)
    ax.set_ylabel("Pressure")
    fig.tight_layout()
    ax = plt.gca()
    ax.invert_yaxis()
    plt.show()

if __name__ == '__main__':
    plotting()
