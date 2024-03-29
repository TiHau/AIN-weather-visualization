import math


def interp(x1, x2, value1, value2, x_res):
    """
    Calculates the interpolated value at x_res
    (((x_res - x1) / (x2 - x1)) * (value2 - value1)) + value1
    :param x1:
    :param x2:
    :param value1:
    :param value2:
    :param x_res: 
    :return: Interpolated value
    """
    tmp1 = (x_res - x1) / (x2 - x1)
    tmp2 = value2 - value1
    tmp3 = tmp1 * tmp2
    y_res = tmp3 + value1
    return y_res


def get_interpolated_value(tl_lat, tl_long, tl_value, tr_lat, tr_long, tr_value, bl_lat, bl_long, bl_value, br_lat,
                           br_long, br_value, lat, long):
    """
    calculates the value of point(lat,long) between the four points tl,tr,bl,br
    :param tl_lat: Latitude of top left corner
    :param tl_long: Longitude of top left corner
    :param tl_value: Value of top left corner
    :param tr_lat: Latitude of top right corner
    :param tr_long: Longitude of top right corner
    :param tr_value: Value of top right corner
    :param bl_lat: Latitude of bottom left corner
    :param bl_long: Longitude of bottom left corner
    :param bl_value: Value of bottom left corner
    :param br_lat: Latitude of bottom right corner
    :param br_long: Longitude of bottom right corner
    :param br_value: Value of bottom right corner
    :param lat: Latitude of the point ot calculate
    :param long: Longitude of the point to calculate
    :return: Value of point(lat,long)
    """
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
