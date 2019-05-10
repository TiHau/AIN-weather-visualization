import matplotlib.pyplot as plt
import numpy as np
import simulation_input as si
import geocalc

# arrival_time: time of arrival as last value on x-axis
# height: highest displayed point above sea level
def plotting(arrival_time):

    # NEEDED FOR VISUALIZATION
    # altitude (y-axis)
    # flight time (x axis)
    # wind speed
    # wind direction
    # elevation (separate plot)

    flight_data = si.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')
    num_points = 10  # number of waypoints

    waypoints = {k: v for (k, v) in flight_data.entry_list.items() if v.is_wp is True}

    print('Num Waypoints: ' + str(len(waypoints)))

    #start_key = list(waypoints.keys())[0]
    #end_key = list(waypoints.keys())[1]

    #section = {k: v for (k, v) in flight_data.entry_list.items() if k in range(start_key, end_key + 1)}
    #step_size = len(section) / num_points
    #section_filtered = []

    #key_index = 1


     #   section_filtered.append(section[round(key_index)])
      #  key_index = key_index + step_size

    #print(len(section_filtered))

    start = (list(waypoints.values())[0].latitude, list(waypoints.values())[0].longitude)
    end = (list(waypoints.values())[1].latitude, list(waypoints.values())[1].longitude)
    print(start, end)

    listAngle = []
    listSpeed = []
    listTime = []
    listAlt = []
    for i in flight_data.entry_list.values():
        listAngle.append(i.wind_angle)
        listSpeed.append(i.wind_speed)
        listTime.append(i.time_stamp)
        listAlt.append(i.attitude)

    listU = []
    listV = []
# calculate u and v values
    indexAngle = 0
    cnt = 0
    for j in listSpeed:
        if cnt > 150:
            listU.append(j * np.cos(listAngle[indexAngle]))
            listV.append(j * np.sin(listAngle[indexAngle]))
            indexAngle += 1
            cnt = 0
        cnt += 1

    print(listU)

    #x = np.linspace(start, end)
    #y = np.linspace(0, max(listAlt))


    # calculate the points on the grid where the wind barbs are to be displayed later
    #xx, yy = np.meshgrid(x, y)
    # creating a matrix for U and V coordinates FOR TEST PURPOSES
    #u, v = xx, yy

    #cnt = 0
    xlist = []
    ylist = []
    #for k in flight_data.entry_list.values():
    #    if cnt > 150:
    #        xlist.append(k.longitude)
    #        ylist.append(k.latitude)
    #        cnt = 0
    #    cnt += 1
    for k in listAlt:
        if cnt > 150:
            ylist.append(k.latitude)
            cnt = 0
        cnt += 1

    print(len(xlist))
    print(len(listU))

    #xarray = np.asarray(xlist)
    #yarray = np.asarray(ylist)

    #x, y = map(xarray, yarray)

    #points = np.meshgrid(y, x)

    fig, ax = plt.subplots()

    # plot barb for each grid coordinate
    plt.barbs(xlist, ylist, np.array(listU), np.array(listV))

    ax.set_xlabel("Strecke")
    ax.set_ylabel("Höhe")

    plt.show()

if __name__ == '__main__':
    plotting(10)
