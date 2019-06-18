import matplotlib.pyplot as plt
import numpy as np
import grib2_extractor as grb
import FlightData as Fd
import util
from matplotlib.ticker import MultipleLocator

def interpolating(flight_data, grib_data, num_waypoints):
    """
    Interpolates over grib_data extracts and FlightData objects
        Args:
            flight_data (FlightData): DateTime. TimeStamp of entry.
            grib_data (dict): extracted data from grib files
            num_waypoints (Integer): number of waypoints to be interpolated over
        Returns:
            res (list): results of interpolation for
            at_waypoint(list): entries for each waypoint in flight_data
        """
    res = []
    at_waypoint = []

    for entry in flight_data.get_path_filtered(num_waypoints):
        tl_lat = util.round_to_nearest_quarter_up(entry.latitude)
        tl_long = util.round_to_nearest_quarter_down(entry.longitude)
        bl_lat = util.round_to_nearest_quarter_down(entry.latitude)
        bl_long = tl_long
        tr_lat = tl_lat
        tr_long = util.round_to_nearest_quarter_up(entry.longitude)
        br_lat = bl_lat
        br_long = tr_long

        grib_data = grib_datas[entry.get_timestamp_of_section()][0]
        grib_data2 = grib_datas[entry.get_timestamp_of_section()][1]

        for key, value in grib_data.items():
            for key2, value2 in value.items():
                for key3, value3 in value2.parameters.items():
                    if grib_data[key][key2].parameters[key3].data != '--':
                        grib_data[key][key2].parameters[key3].data = (value3.data + grib_data2[key][key2].parameters[
                            key3].data) / 2

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
                    ip = util.get_interpolated_value(tl_lat, tl_long, tl_param.data, tr_lat, tr_long, tr_param.data,
                                                     bl_lat, bl_long, bl_param.data, br_lat, br_long, br_param.data,
                                                     entry.latitude, entry.longitude)
                    res_values.append((level.level, level.name, tl_param.name, tl_param.unit, ip))
                except:
                    pass
        res.append(res_values)
    return res, at_waypoint


def plotting(num_waypoints_or_timestamps, res, at_entry, waypoints):
    """
        Analyzes the data that is given as argument and displays it in a plot
        Args:
            num_waypoints_or_timestamps (Integer): Number of waypoints/timestamps to be plotted
            res (list): result res of function interpolating()
            at_entry (list): result at_waypoint of function interpolating()
            waypoints (Boolean): Set to true if you want to see the waypoints on x-axis, false if you need timestamps
        """

    # quick exception handling
    if num_waypoints_or_timestamps == 0:
        print("Number of waypoints must be higher than 0")
        exit(1)

    # constants
    FEET_TO_METERS = 0.305
    UPPER_LIMIT = 1000
    LOWER_LIMIT = 50
    KELVIN_TO_CELSIUS = 273

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
                    temperature[val[0]].append(val[4] - KELVIN_TO_CELSIUS)

    # preparing temperature for plotting
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

    # Plotting temperature
    fig, ax = plt.subplots()
    ax1 = fig.add_subplot(111, sharex=ax)
    im = ax1.imshow(heat_array, extent=[0,num_waypoints_or_timestamps+1,0,num_waypoints_or_timestamps], cmap='plasma')

    # Plotting wind barbs
    ax2 = ax1.twinx()
    lvl_cnt = 0
    for lvl in u_comp.keys():
        lvl_cnt += 1
        ax2.barbs(np.arange(1, num_waypoints_or_timestamps + 1), lvl, np.array(u_comp.get(lvl)), np.array(v_comp.get(lvl)),
                 length=5.5, rasterized=True)

    # adding grid lines
    spacing = 50
    minorLocator = MultipleLocator(spacing)
    ax2.yaxis.set_minor_locator(minorLocator)
    ax2.grid(which='minor')

    # plotting altitude of vehicle
    ax2.plot(np.arange(1, num_waypoints_or_timestamps + 1, step=1), result_pressure_height, color='red')
    ax2 = plt.gca()
    ax2.invert_yaxis()

    # setting ticks and labels correctly
    ax2.set_xticks(np.arange(1, num_waypoints_or_timestamps + 1, step=1))
    ax2.set_xticklabels(xlabels)
    ax2.set_ylabel("Pressure (hPa)")
    ax.axes.get_yaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    if waypoints:
        ax1.set_xlabel("Waypoints (lat/lon)")
    else:
        ax1.set_xlabel("Timestamps (Datetime)")

    # adding color bar on the left side of the plot
    cbaxes = fig.add_axes([0.02, 0.15, 0.03, 0.7])
    cbaxes.set_xlabel("Temp. (°C)")
    cb = plt.colorbar(im, cax=cbaxes)

    plt.show()


if __name__ == '__main__':

    flight_data = Fd.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')

    grib_datas = {}

    for key in flight_data.split_in_timesecions().keys():
        grib_datas[key] = [grb.import_from_json(
            'grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f003.json')]
        grib_datas[key].append(grb.import_from_json(
            'grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f006.json'))


    res, wp = interpolating(flight_data, grib_datas, 10)
    plotting(10, res, wp, False)
