import math

EARTH_RADIUS = 6371e3  # meters


def calculate_initial_compass_bearing(point_a, point_b):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `point_a: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `point_b: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(point_a) != tuple) or (type(point_b) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    diff_long = math.radians(point_b[1] - point_a[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # normalize the initial bearing
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def create_cord(coord, bearing, distance):
    """
        Calculates a new Coord (distance) meters away from (coord) with (bearing).
        The formulae used is the following:
            φ2 = asin( sin φ1 ⋅ cos δ + cos φ1 ⋅ sin δ ⋅ cos θ )
            λ2 = λ1 + atan2( sin θ ⋅ sin δ ⋅ cos φ1, cos δ − sin φ1 ⋅ sin φ2 )
        :Parameters:
          - `coord: The tuple representing the latitude/longitude for the
            point. Latitude and longitude must be in decimal degrees
          - `bearing: The float representing the bearing for coord.
            Bearing must be in decimal degrees
          - `distance: The distance in meters
        :Returns:
          The latitude/longitude in degrees
        :Returns Type:
          (float, float)
        """
    if type(coord) != tuple:
        raise TypeError("Only a tuple is supported as arguments coord")

    angular_distance = distance / EARTH_RADIUS  # angular distance in radians
    bearing = math.radians(bearing)
    lat = math.radians(coord[0])
    long = math.radians(coord[1])

    new_lat = math.asin(
        math.sin(lat) * math.cos(angular_distance) + math.cos(lat) * math.sin(angular_distance) * math.cos(bearing))
    # λ2 = λ1 + atan2( sin θ ⋅ sin δ ⋅ cos φ1, cos δ − sin φ1 ⋅ sin φ2 )
    new_long = long + math.atan2(math.sin(bearing) * math.sin(angular_distance) * math.cos(lat),
                                 math.cos(angular_distance) - math.sin(lat) * math.sin(new_lat))
    # normalise to - 180.. + 180°
    new_long = (new_long + 3 * math.pi) % (2 * math.pi) - math.pi

    return math.degrees(new_lat), math.degrees(new_long)


def calculate_distance(point_a, point_b):
    """
        Calculates the bearing between two points.
        The formulae used is the following:
            a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
            c = 2 ⋅ atan2( √a, √(1−a) )
            d = R ⋅ c
        :Parameters:
          - `point_a: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `point_b: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
          The distance in meters
        :Returns Type:
          float
        """
    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    d_lon = math.radians(point_b[1] - point_a[1])
    distance = math.acos(
        math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(d_lon)) * EARTH_RADIUS

    return distance


if __name__ == '__main__':
    constance = (47.66033, 9.17582)
    munich = (48.137154, 11.576124)

    d_con_mun = calculate_distance(constance, munich)
    b_con_mun = calculate_initial_compass_bearing(constance, munich)

    print('Distance constance -> munich' + str(d_con_mun))
    print('Bearing constance -> munich' + str(b_con_mun))

    for i in range(0, 11):
        co = create_cord(constance, b_con_mun, (d_con_mun / 10) * i)
        print(str(round(co[0], 6)) + ', ' + str(round(co[1], 6)))
