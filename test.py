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
    tl = geocalc.LatLongValue(10.25, 20, 40)
    tr = geocalc.LatLongValue(10.25, 20.25, 21.5)
    bl = geocalc.LatLongValue(10, 20, 20)
    br = geocalc.LatLongValue(10, 20.25, 20.5)

    lat = 10.12
    long = 20.2

    test_res = geocalc.get_interpolated_value(tl, tr, bl, br, lat, long)

    print(test_res)

    print(geocalc.round_to_nearest_quarter_up(12.2))
    print(geocalc.round_to_nearest_quarter_down(12.2))


def test_simulation():
    flight_data = si.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')

    flight_data.get_waypoints()

    print(flight_data.get_path_filtered(10))

    print(flight_data.get_max_latitude())
    print(flight_data.get_min_latitude())
    print(flight_data.get_max_longitude())
    print(flight_data.get_min_longitude())

    path, grib_data = grib2_extractor.extract('gfs.t00z.pgrb2.0p25.f003', geocalc.round_to_nearest_quarter_down(flight_data.get_min_latitude()),
                                        geocalc.round_to_nearest_quarter_down(flight_data.get_min_longitude()), geocalc.round_to_nearest_quarter_up(flight_data.get_max_latitude()),
                                        geocalc.round_to_nearest_quarter_up(flight_data.get_max_longitude()), ["wind", "pressure", "height", "temp"])

    grib2_extractor.export_to_json(grib_data, path)
    js = grib2_extractor.import_from_json(path + ".json")
    print()

if __name__ == '__main__':
    # test_geocalc()
    test_simulation()
