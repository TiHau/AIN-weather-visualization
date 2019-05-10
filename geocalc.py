import math

EARTH_RADIUS = 6371e3  # meters


class LatLongValue:
    def __init__(self, lat_init, long_init, value_init):
        self.lat = float(lat_init)
        self.long = float(long_init)
        self.value = float(value_init)

    def __repr__(self):
        return 'Point[ lat:' + str(self.lat) + "| long: " + str(self.long) + "| Value: " + str(self.value) + "]"


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


def interp(x1, x2, y1, y2, x_res):
    v1 = (x_res - x1) / (x2 - x1)
    v2 = y2 - y1
    v3 = v1 * v2
    res = v3 + y1
    return res


def get_interpolated_value(tl_lat, tl_long, tl_value, tr_lat, tr_long, tr_value, bl_lat, bl_long, bl_value, br_lat, br_long, br_value, lat, long):
    x1 = min(tl_lat, bl_lat)
    x2 = max(tl_lat, bl_lat)
    x3 = lat
    y1 = min(tl_value, bl_value)
    y2 = max(tl_value, bl_value)
    middle_value_left = interp(x1, x2, y1, y2, x3)

    x1 = min(tr_lat, br_lat)
    x2 = max(tr_lat, br_lat)
    x3 = lat
    y1 = min(tr_value, br_value)
    y2 = max(tr_value, br_value)
    middle_value_right = interp(x1, x2, y1, y2, x3)

    x1 = min(bl_long, br_long)
    x2 = max(bl_long, br_long)
    x3 = long
    y1 = min(middle_value_left, middle_value_right)
    y2 = max(middle_value_left, middle_value_right)
    first_res = interp(x1, x2, y1, y2, x3)

    x1 = min(tl_long, tr_long)
    x2 = max(tl_long, tr_long)
    x3 = long
    y1 = min(tl_value, tr_value)
    y2 = max(tl_value, tr_value)
    middle_value_top = interp(x1, x2, y1, y2, x3)

    x1 = min(bl_long, br_long)
    x2 = max(bl_long, br_long)
    x3 = long
    y1 = min(bl_value, br_value)
    y2 = max(bl_value, br_value)
    middle_value_bottom = interp(x1, x2, y1, y2, x3)

    x1 = min(bl_lat, tl_lat)
    x2 = max(bl_lat, tl_lat)
    x3 = lat
    y1 = min(middle_value_bottom, middle_value_top)
    y2 = max(middle_value_right, middle_value_top)
    second_res = interp(x1, x2, y1, y2, x3)

    return (first_res + second_res) / 2


def round_to_nearest_quarter_down(value):
    return math.floor(value * 4) / 4


def round_to_nearest_quarter_up(value):
    return math.ceil(value * 4) / 4
