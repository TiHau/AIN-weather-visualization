import pygrib as grib
import json


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


def extract(file_path, lat1, lon1, lat2, lon2, list_params_extract):
    """extracts data from gfs file and save it into extractor dictionary
        the extracted data is between the coordinate1 and coordinate2

        Args:
                file_path (str): path to grib2 file.
                lat1 (float): minimal latitude.
                lon1 (float): minimal longitude.
                lat2 (float): maximal latitude.
                lon2 (float): maximal latitude.
                list_params_extract (list): Match pattern list for parameters
        Returns:
                the extractor dict for each coordinate raster position with parameters and the file name

                   """

    coordinate1 = (lat1, lon1)
    coordinate2 = (lat2, lon2)

    data_params_to_extract = list_params_extract
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

    return file_path, position


def export_to_json(dictionary, json_name):
    """exports an extracted dict to json

          Args:
                  dictionary (dict): dictionary to convert.
                  json_name (str): filename of the json write to

                     """
    with open(json_name + ".json", "w+") as my_json:
        content = {}
        for entry in dictionary.keys():
            content[str(entry)] = {}
            for level in dictionary.get(entry).keys():
                content[str(entry)][str(level)] = {}
                level_class = dictionary.get(entry).get(level)
                content[str(entry)][str(level)]["name"] = str(level_class.name)
                content[str(entry)][str(level)]["level"] = str(level_class.level)
                content[str(entry)][str(level)]["parameters"] = {}
                for parameter in dictionary.get(entry).get(level).parameters:
                    content[str(entry)][str(level)]["parameters"][str(parameter)] = {}
                    parameter_class = dictionary.get(entry).get(level).parameters.get(parameter)
                    content[str(entry)][str(level)]["parameters"][str(parameter)]["name"] = str(parameter_class.name)
                    content[str(entry)][str(level)]["parameters"][str(parameter)]["data"] = str(parameter_class.data)
                    content[str(entry)][str(level)]["parameters"][str(parameter)]["unit"] = str(parameter_class.unit)
        my_json.write(json.dumps(content))


def import_from_json(file_path):
    """converts an json file back to an extractor dict

          Args:
                  file_path (str): path of the json file.
          Returns:
                  the  extractor dict for each coordinate raster position with parameters and the file name

                     """
    position = {}
    with open(file_path) as my_json:
        data = json.load(my_json)
        for p in data:
            point = tuple(map(float, p[1:-1].split(',')))
            position[point] = {}
            for l in data[p]:
                level = int(l)
                position[point][level] = Level(level, data[p][l]["name"])
                for param in data[p][l]["parameters"]:
                    try:
                        position[point].get(level).add_parameter(
                            Parameter(data[p][l]["parameters"][param]["name"],
                                      float(data[p][l]["parameters"][param]["data"]),
                                      data[p][l]["parameters"][param]["unit"]))


                    except:
                        position[point].get(level).add_parameter(
                            Parameter(data[p][l]["parameters"][param]["name"],
                                      data[p][l]["parameters"][param]["data"],
                                      data[p][l]["parameters"][param]["unit"]))

    return position