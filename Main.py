import os

import grib2_extractor as grb
import util
from plotting import plotting
import downloader
import FlightData as Fd

if __name__ == '__main__':

    flight_data = Fd.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')
    tmp_list = list(flight_data.entry_list.values())
    first_ts = tmp_list[0].get_timestamp_of_section()
    last_ts = tmp_list[len(tmp_list) - 1].get_timestamp_of_section()
    downloader.download(first_ts, last_ts)


    for key in flight_data.split_in_timesecions().keys():
        try:
            open('grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f003.json', 'r')
            os.remove('grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f003.json')
            open('grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f006.json', 'r')
            os.remove('grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f006.json')
        except FileNotFoundError:
            pass
        path, grib_data = grb.extract('grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f003.json',
                                            util.round_to_nearest_quarter_down(flight_data.get_min_latitude()),
                                            util.round_to_nearest_quarter_down(flight_data.get_min_longitude()),
                                            util.round_to_nearest_quarter_up(flight_data.get_max_latitude()),
                                            util.round_to_nearest_quarter_up(flight_data.get_max_longitude()),["wind", "height", "temp"])
        grb.export_to_json(grib_data, path + ".json")
        path, grib_data = grb.extract(
            'grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f006.json',
            util.round_to_nearest_quarter_down(flight_data.get_min_latitude()),
            util.round_to_nearest_quarter_down(flight_data.get_min_longitude()),
            util.round_to_nearest_quarter_up(flight_data.get_max_latitude()),
            util.round_to_nearest_quarter_up(flight_data.get_max_longitude()), ["wind", "height", "temp"])
        grb.export_to_json(grib_data, path + ".json")


    grib_datas = {}

    for key in flight_data.split_in_timesecions().keys():
        grib_datas[key] = [grb.import_from_json(
            'grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f003.json')]
        grib_datas[key].append(grb.import_from_json(
            'grib2_files/' + key.strftime('%Y-%m-%d') + '/gfs.t' + key.strftime('%H') + 'z.pgrb2.0p25.f006.json'))

    res = []
    at_waypoint = []

    for entry in flight_data.get_path_filtered(10):
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
    plotting(10, res, at_waypoint, False)
