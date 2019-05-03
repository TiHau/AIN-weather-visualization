import simulation_input as si
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


if __name__ == '__main__':
    # test_geocalc()
    flight_data = si.read('2019-05-01_EDDM-EDDH_Aviator.tsv')

    print(flight_data.entry_list[1].latitude)

    waypoints = {k: v for (k, v) in flight_data.entry_list.items() if v.is_wp is True}

    print(len(waypoints))

    t = list(waypoints.keys())

    print(t)

    start = (list(waypoints.values())[0].latitude, list(waypoints.values())[0].longitude)
    end = (list(waypoints.values())[1].latitude, list(waypoints.values())[1].longitude)
    print(start, end)
