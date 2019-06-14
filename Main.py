import os

import grib2_extractor as grb
import util
from plotting import plotting
from plotting import interpolating
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

    res, wp = interpolating(flight_data, grib_datas, 10)
    plotting(10, res, wp, False)
