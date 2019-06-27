import datetime
import os

import grib2_extractor as grb
import util
from plotting import plotting
import downloader
import FlightData as Fd
from threading import Thread

if __name__ == '__main__':
    NUM_POINTS = 10
    WAYPOINTS_OR_TIME = False  # False = Time, True = Waypoint
    SIMULATION_FILE = '2019-05-01_EDDM-EDDH_Aviator.tsv'

    # Load Flight Data
    flight_data = Fd.FlightData(SIMULATION_FILE)
    tmp_list = list(flight_data.entry_list.values())
    first_ts = tmp_list[0].get_timestamp_of_section()
    first_ts -= datetime.timedelta(hours=6)
    last_ts = tmp_list[len(tmp_list) - 1].get_timestamp_of_section()
    # Download needed gfs files
    downloader.download(first_ts, last_ts)

    # Remove old Json files and export new ones
    for file in [pos_json for pos_json in os.listdir('grib2_files/' + last_ts.strftime('%Y-%m-%d')) if pos_json.endswith ('.json')]:
        try:
            open('grib2_files/' + last_ts.strftime('%Y-%m-%d') + '/' + file, 'r')
            print('removed file: ' + file)
            os.remove('grib2_files/' + last_ts.strftime('%Y-%m-%d') + '/' + file)
        except FileNotFoundError:
            pass
    arr = os.listdir('grib2_files/' + last_ts.strftime('%Y-%m-%d'))
    threads = []
    def procedure(file):
        path, grib_data = grb.extract('grib2_files/' + last_ts.strftime('%Y-%m-%d') + '/' + file,
                                      util.round_to_nearest_quarter_down(flight_data.get_min_latitude()),
                                      util.round_to_nearest_quarter_down(flight_data.get_min_longitude()),
                                      util.round_to_nearest_quarter_up(flight_data.get_max_latitude()),
                                      util.round_to_nearest_quarter_up(flight_data.get_max_longitude()),
                                      ["wind", "height", "temp"])
        grb.export_to_json(grib_data, path)

    for file in arr:
        print("extract " + file)
        t = Thread(target=procedure, args=(file,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # import data from Json files
    grib_datas = {}

    for timestamp in flight_data.split_in_timesections():
        real_timestamp = timestamp
        if timestamp.hour in {3, 9, 15, 21}:
            timestamp -= datetime.timedelta(hours=3)
            hours_in_future = 3
        else:
            timestamp -= datetime.timedelta(hours=6)
            hours_in_future = 6

        grib_datas[real_timestamp] = grb.import_from_json(
            'grib2_files/' + timestamp.strftime('%Y-%m-%d') + '/gfs.t' + timestamp.strftime(
                '%H') + 'z.pgrb2.0p25.f00' + str(hours_in_future) + '.json')

    # Interpolate data
    res = []
    at_waypoint = []

    for entry in flight_data.get_path_filtered(NUM_POINTS):

        grib_data_timestamp = entry.get_timestamp_of_section()
        grib_data_future_timestamp = grib_data_timestamp + datetime.timedelta(hours=3)

        grib_data = grib_datas[grib_data_timestamp]
        grib_data_future = grib_datas[grib_data_future_timestamp]

        # Time interpolation
        for key, value in grib_data.items():
            for key2, value2 in value.items():
                for key3, value3 in value2.parameters.items():
                    try:
                        if grib_data_future[key][key2].parameters[key3].data != '--' and value3.data != '--':
                            x1 = float(0)
                            x2 = datetime.timedelta(hours=3).total_seconds()
                            x_res = (grib_data_future_timestamp - entry.timestamp).total_seconds()

                            grib_data[key][key2].parameters[key3].data = util.interp(x1, x2, value3.data,
                                                                                     grib_data_future[key][
                                                                                         key2].parameters[
                                                                                         key3].data, x_res)
                    except:
                        print('Key Error')

        # Geo interpolation
        tl_lat = util.round_to_nearest_quarter_up(entry.latitude)
        tl_long = util.round_to_nearest_quarter_down(entry.longitude)
        bl_lat = util.round_to_nearest_quarter_down(entry.latitude)
        bl_long = tl_long
        tr_lat = tl_lat
        tr_long = util.round_to_nearest_quarter_up(entry.longitude)
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
                    ip = util.get_interpolated_value(tl_lat, tl_long, tl_param.data, tr_lat, tr_long, tr_param.data,
                                                     bl_lat, bl_long, bl_param.data, br_lat, br_long, br_param.data,
                                                     entry.latitude, entry.longitude)
                    res_values.append((level.level, level.name, tl_param.name, tl_param.unit, ip))
                except:
                    pass
        res.append(res_values)
    # plot data
    plotting(NUM_POINTS, res, at_waypoint, False)
