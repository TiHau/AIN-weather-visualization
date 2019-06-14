import matplotlib.pyplot as plt
import numpy as np
import util



# arrival_time: time of arrival as last value on x-axis
# height: highest displayed point above sea level
def plotting(num_waypoints_or_timestamps, res, at_entry, waypoints):

    #exception handling
    if num_waypoints_or_timestamps == 0:
        print("Number of waypoints must be higher than 0")
        exit(1)

    # constants
    FEET_TO_METERS = 0.305
    UPPER_LIMIT = 1000
    LOWER_LIMIT = 50

    # getti
    #res = []
    #at_waypoint = []



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
    fig, ax = plt.subplots()

    ax1 = fig.add_subplot(111, sharex=ax)


    heat_array = []
    lvl_cnt = 0
    for lvl in u_comp.keys():
        lvl_cnt += 1
        heat_array.append(temperature.get(lvl))

    # Höhe
    height_pressure_upper = {}
    height_upper = {}
    height_pressure_lower = {}

    height_lower = {}
    height_original = []

    index = 0
    xlabels = []

    for entry in at_entry:
        if waypoints:
            xlabels.append(str(entry.latitude) + ",\n " + str(entry.longitude))
        else:
            xlabels.append(entry.time_stamp.strftime("%d/%m/%y\n%H:%M:%S"))
            #xlabels.append(str(entry.time_stamp))
        height_pressure_upper[index+1] = []
        height_upper[index+1] = []
        height_pressure_lower[index+1] = []
        height_lower[index + 1] = []
        height_original.append(entry.attitude*FEET_TO_METERS)
        for (k, v) in heights.items():
            if v[index] > entry.attitude*FEET_TO_METERS:
                height_upper[index+1].append(v[index])
                height_pressure_upper[index+1].append(k)
            if v[index] <= entry.attitude*FEET_TO_METERS:
                height_lower[index + 1].append(v[index])
                height_pressure_lower[index+1].append(k)
        index += 1


    pressure_upper = []
    for entry in height_pressure_upper.values():
        try:
            pressure_upper.append(entry[len(entry)-1])
        except IndexError:
            pass
    height_tmp_upper = []
    for entry in height_upper.values():
        try:
            height_tmp_upper.append(entry[len(entry) - 1])
        except IndexError:
            pass
    pressure_lower = []
    for entry in height_pressure_lower.values():
        try:
            pressure_lower.append(entry[0])
        except IndexError:
            pressure_lower.append(UPPER_LIMIT)
    height_tmp_lower = []
    for entry in height_lower.values():
        try:
            height_tmp_lower.append(entry[0])
        except IndexError:
            height_tmp_lower.append(float(0.0))
    # calculate pressure to height of vehicle
    result_pressure_height = []
    for i in np.arange(0, num_waypoints_or_timestamps, step=1):
        lower_h = float(height_tmp_lower[i])
        upper_h = float(height_tmp_upper[i])
        original = float(height_original[i])
        lower_p = float(pressure_lower[i])
        upper_p = float(pressure_upper[i])
        if lower_h == original:
            result_pressure_height.append(lower_p)
        else:
            one_percent_h = (upper_h - lower_h) / 100
            percent_of_diff = (original - lower_h) / one_percent_h
            one_percent_p = (upper_p - lower_p) / 100
            add_to_lower = one_percent_p * percent_of_diff
            result_pressure_height.append(lower_p + add_to_lower)

    # Temperature
    im = ax1.imshow(heat_array, extent=[0,num_waypoints_or_timestamps+1,0,num_waypoints_or_timestamps], cmap='plasma')

    ax2 = ax1.twinx()
    lvl_cnt = 0
    for lvl in u_comp.keys():
        lvl_cnt += 1
        ax2.barbs(np.arange(1, num_waypoints_or_timestamps + 1), lvl, np.array(u_comp.get(lvl)), np.array(v_comp.get(lvl)),
                 length=5.5, rasterized=True)

    ax2.grid()
    ax2.plot(np.arange(1, num_waypoints_or_timestamps + 1, step=1), result_pressure_height, color='red')
    ax2 = plt.gca()
    ax2.invert_yaxis()

    ax2.set_xticks(np.arange(1, num_waypoints_or_timestamps + 1, step=1))
    ax2.set_xticklabels(xlabels)
    ax2.set_ylabel("Pressure (hPa)")
    ax.axes.get_yaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    cbaxes = fig.add_axes([0.02, 0.15, 0.03, 0.7])  # This is the position for the colorbar
    cbaxes.set_xlabel("Temp. (K)")
    cb = plt.colorbar(im, cax=cbaxes)

    if waypoints:
        ax1.set_xlabel("Waypoints (lat/lon)")
    else:
        ax1.set_xlabel("Timestamps (Datetime)")


    plt.show()


