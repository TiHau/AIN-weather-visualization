import pygrib as grib

class Level:
    """Init's a new level.
        Args:
            level (int): Integer of the level.
            name (str)j: Name of the level.

        Attributes:
            level (int): Integer of the level.
            name (str)j: Name of the level.

        """

    def __init__(self, level, name):
        self.level = level
        self.name = name
        self.parameters = {}

    def add_parameter(self, parameter):
        """adds an parameter to parameters dictionary
            Args:
                parameter (Parameter): an Parameter

                      """
        self.parameters[parameter.name] = parameter

    def __repr__(self):
        """overrides the string output of level recursive

                      Returns:
                          the level class as string recursive.

                      """
        return str(self.__dict__)


class Parameter:
    """Init's a new parameter.
            Args:
                name (str): Name of the parameter.
                data (float): Value of the parameter.
                unit (str): Unit of the parameter

            Attributes:
                name (str): Name of the parameter.
                data (float): Value of the parameter.
                unit (str): Unit of the parameter

            """

    def __init__(self, name, data, unit):
        self.name = name
        self.data = data
        self.unit = unit

    def __repr__(self):
        """overrides the string output of parameter recursive

                Returns:
                    the parameter class as string recursive.

                """
        return str(self.__dict__)


def extract(file_path, lat1, lon1, lat2, lon2):
    """extracts data from gfs file and save it into position map
        the extracted data is between the coordinate1 and coordinate2

        Args:
                file_path (str): path to grib2 file.
                data (float): Value of the parameter.
                unit (str): Unit of the parameter
        Returns:
                the map for each coordinate raster position with parameters

                   """

    coordinate1 = (lat1, lon1)
    coordinate2 = (lat2, lon2)

    data_params_to_extract = ["wind", "pressure", "height"]
    f = grib.open(file_path)

    position = {}
    lats = []
    lons = []

    for lines in f:
        tmp = str(lines).split(':')[:2]
        if any(dataParamToExtract in tmp[1].lower() for dataParamToExtract in data_params_to_extract):
            print(tmp)
            g = f[int(tmp[0])]
            type_of_level = g.typeOfLevel
            level = g.level
            name = g.name
            data_array = g.data(coordinate1[0], coordinate2[0], coordinate1[1], coordinate2[1])
            data = data_array[0]
            unit = g.parameterUnits
            if len(lats) == 0:
                for latArrays in data_array[1]:
                    lats.append(latArrays[0])
                for lon in data_array[2]:
                    for l in lon:
                        lons.append(l)
                    break
            lat_index = 0
            for lat in lats:
                lon_index = 0
                for lon in lons:
                    if (lat, lon) not in position:
                        position[(lat, lon)] = {}
                    if level not in position[(lat, lon)]:
                        position[(lat, lon)][level] = Level(level, type_of_level)
                    if name not in position[(lat, lon)].get(level).parameters:
                        position[(lat, lon)].get(level).add_parameter(
                            Parameter(name, data[lat_index][lon_index], unit))
                    lon_index += 1
                lat_index += 1
    return position
