import simulation_input as si
import geocalc


# import grib2_extractor


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
    num_points = 10

    waypoints = {k: v for (k, v) in flight_data.entry_list.items() if v.is_wp is True}

    print('Num Waypoints: ' + str(len(waypoints)))

    start_key = list(waypoints.keys())[0]
    end_key = list(waypoints.keys())[1]
    section = {k: v for (k, v) in flight_data.entry_list.items() if k in range(start_key, end_key + 1)}
    step_size = len(section) / num_points
    section_filtered = []

    key_index = 1

    for i in range(1, num_points + 1):
        section_filtered.append(section[round(key_index)])
        key_index = key_index + step_size

    print(len(section_filtered))

    start = (list(waypoints.values())[0].latitude, list(waypoints.values())[0].longitude)
    end = (list(waypoints.values())[1].latitude, list(waypoints.values())[1].longitude)
    print(start, end)
    print(section_filtered)
    # grib_data = grib2_extractor.extract("gfs.t12z.pgrb2.0p25.f003", list(waypoints.values())[0].latitude, list(waypoints.values())[0].longitude, list(waypoints.values())[1].latitude, list(waypoints.values())[1].longitude)


if __name__ == '__main__':
    # test_geocalc()
    test_simulation()
