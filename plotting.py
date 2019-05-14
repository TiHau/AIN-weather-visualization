import matplotlib.dates as dat
import matplotlib.pyplot as plt
import numpy as np
import grib2_extractor as grb
import FlightData as Fd
import datetime as dt
import time

# arrival_time: time of arrival as last value on x-axis
# height: highest displayed point above sea level
def plotting():

    # NEEDED FOR VISUALIZATION
    # altitude (y-axis)
    # flight time (x axis)
    # wind speed
    # wind direction
    # elevation (separate plot)

    flight_data = Fd.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')

    # Getting waypoints (irrelevant for now)
    #num_points = 10  # number of waypoints

    #waypoints = {k: v for (k, v) in flight_data.entry_list.items() if v.is_wp is True}

    #print('Num Waypoints: ' + str(len(waypoints)))

    #start_key = list(waypoints.keys())[0]
    #end_key = list(waypoints.keys())[1]

    #section = {k: v for (k, v) in flight_data.entry_list.items() if k in range(start_key, end_key + 1)}
    #step_size = len(section) / num_points
    #section_filtered = []

    #key_index = 1


     #   section_filtered.append(section[round(key_index)])
      #  key_index = key_index + step_size

    #print(len(section_filtered))

    #start = (list(waypoints.values())[0].latitude, list(waypoints.values())[0].longitude)
    #end = (list(waypoints.values())[1].latitude, list(waypoints.values())[1].longitude)


    # Getting the needed values inside a list: Altitude, flight time, angle and speed
    list_angle = []
    list_speed = []
    list_time = []
    list_alt = []
    for i in flight_data.entry_list.values():
        list_angle.append(i.wind_angle)
        list_speed.append(i.wind_speed)
        list_time.append(i.time_stamp)
        list_alt.append(i.attitude)

    print(str(len(list_angle)), str(len(list_speed)), str(len(list_time)), str(len(list_alt)))
# calculate u and v values (needed for barb plotting)
    list_u = []
    list_v = []
    index_angle = 0
    cnt = 0
    for j in list_speed:
        if cnt > 74:  # ensure that the arrays have a length of 12 FOR TESTING PURPOSE
            list_u.append(j * np.cos(list_angle[index_angle]))
            list_v.append(j * np.sin(list_angle[index_angle]))
            index_angle += 1
            cnt = 0
        cnt += 1

    print(list_time)
    y = np.linspace(0, 60000, 12)
    x = np.linspace(0, len(list_time), 12)

    # calculate the points on the grid where the wind barbs are to be displayed later
    xx, yy = np.meshgrid(x, y)

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

    fig, ax = plt.subplots()

    # plot altitude depending on time
    new_time = []
    for t in list_time:
        new_time.append(dt.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f'))

    print("Lengths:" + str(len(xx)) + " " + str(len(yy)) + " " + str(len(np.array(list_u))) + " " + str(len(np.array(list_v))))

    # plot barb for each grid coordinate
    #plt.barbs(x, y, np.array(list_u), np.array(list_v))

    # Flughöhe in Metern anzeigen

    ax.plot(new_time, list_alt)
    plt.gcf().autofmt_xdate()

    ax.set_ylim([0, 60000])
    ax.set_xlabel("Flugzeit")
    ax.set_ylabel("Höhe")
    fig.tight_layout()

    plt.show()


if __name__ == '__main__':
    plotting()
