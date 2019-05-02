import geocalc

if __name__ == '__main__':
    # Test cord creation
    constance = (47.66033, 9.17582)
    munich = (48.137154, 11.576124)

    d_con_mun = geocalc.calculate_distance(constance, munich)
    b_con_mun = geocalc.calculate_initial_compass_bearing(constance, munich)

    print('Distance constance -> munich' + str(d_con_mun))
    print('Bearing constance -> munich' + str(b_con_mun))

    for i in range(0, 11):
        co = geocalc.create_cord(constance, b_con_mun, (d_con_mun / 10) * i)
        print(str(round(co[0], 6)) + ', ' + str(round(co[1], 6)))

    # Test interpolation
    tl = geocalc.LatLongValue(10.25, 20, 21)
    tr = geocalc.LatLongValue(10.25, 20.25, 21.5)
    bl = geocalc.LatLongValue(10, 20, 20)
    br = geocalc.LatLongValue(10, 20.25, 20.5)

    lat = 10.12
    long = 20.2

    test_res = geocalc.get_interpolated_value(tl, tr, bl, br, lat, long)

    print(test_res)