import FlightData as si
import geocalc
import grib2_extractor


def test_geocalc():
    # Test cord creation
    constance = (47.66033, 9.17582)
    munich = (48.137154, 11.576124)

    d_con_mun = geocalc.calculate_distance(constance, munich)
    b_con_mun = geocalc.calculate_initial_compass_bearing(constance, munich)

    print('Distance constance -> munich ' + str(d_con_mun))
    print('Bearing constance -> munich ' + str(b_con_mun))

    for i in range(0, 11):
        co = geocalc.create_cord(constance, b_con_mun, (d_con_mun / 10) * i)
        print(str(round(co[0], 6)) + ', ' + str(round(co[1], 6)))

    # Test interpolation
    lat = 10.12
    long = 20.2

    test_res = geocalc.get_interpolated_value(10.25, 20, 40, 10.25, 20.25, 21.5, 10, 20, 20, 10, 20.25, 20.5, lat, long)

    print(test_res)

    # Test round
    print(geocalc.round_to_nearest_quarter_up(12.2))
    print(geocalc.round_to_nearest_quarter_down(12.2))


def test_simulation():
    flight_data = si.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')

    grib_data = grib2_extractor.extract('gfs.t12z.pgrb2.0p25.f003',
                                        geocalc.round_to_nearest_quarter_down(flight_data.get_min_latitude()),
                                        geocalc.round_to_nearest_quarter_down(flight_data.get_min_longitude()),
                                        geocalc.round_to_nearest_quarter_up(flight_data.get_max_latitude()),
                                        geocalc.round_to_nearest_quarter_up(flight_data.get_max_longitude()))

    res = []

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

        res_values = []

        for level in tl_grib_values.values():
            for tl_param in level.parameters.values():
                bl_param = bl_grib_values[level.level].parameters[tl_param.name]
                tr_param = tr_grib_values[level.level].parameters[tl_param.name]
                br_param = br_grib_values[level.level].parameters[tl_param.name]

                ip = geocalc.get_interpolated_value(tl_lat, tl_long, tl_param.data, tr_lat, tr_long, tr_param.data,
                                                    bl_lat, bl_long, bl_param.data, br_lat, br_long, br_param.data,
                                                    entry.latitude, entry.longitude)
                res_values.append((level.level, tl_param.name, tl_param.unit, ip))

        res.append((entry, res_values))

    print(res)


if __name__ == '__main__':
    test_geocalc()
    # test_simulation()
