import pygrib as grib
import struct
import numpy as np
import csv
import json


class Level:
    """Init's a new level.
        Args:
            level (int): Integer of the level.
            type (str)j: Name of the level.

        Attributes:
            level (int): Integer of the level.
            type (str)j: Name of the level.

        """
    def __init__(self, level, type):
        self.level = level
        self.type = type
        self.parameters = {}

    def addParameter(self, parameter):
        self.parameters[parameter.name] = parameter

    def __repr__(self):
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


def extract():
    """extracts data from gfs file and save it into position map
        the extracted data is between the coordinate1 and coordinate2
                   """
    file = 'gfs.t00z.pgrb2.0p25.f003'  # example filename
    coordinate1 = (4,5)#(47.66033, 9.17582)
    coordinate2 = (5,6)#(48.137154, 11.576124)
    dataParamsToExtract = ["wind", "pressure", "height"]
    f = grib.open(file)
    g = f.message(1)
    json_name = str(g.validDate) + "-" + str(
        g.analDate) + "-" + str(g.forecastTime) + ":lat1:" + str(
        coordinate1[0]) + ":lat2:" + str(coordinate2[0]) + ":lon1:" + str(
        coordinate1[1]) + ":lon1:" + str(coordinate2[1])

    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    print(json_name)
    position = {}
    lats = []
    lons = []

    with open(json_name + ".json", "w+") as my_json:
        for lines in f:
            tmp = str(lines).split(':')[:2]
            if any(dataParamToExtract in tmp[1].lower() for dataParamToExtract in dataParamsToExtract):
                print(tmp)
                g = f[int(tmp[0])]
                typeOfLevel = g.typeOfLevel
                level = g.level
                name = g.name
                dataArray = g.data(coordinate1[0], coordinate2[0], coordinate1[1], coordinate2[1])
                data = dataArray[0]
                unit = g.parameterUnits
                if len(lats) == 0:
                    for latArrays in dataArray[1]:
                        lats.append(latArrays[0])
                    for lon in dataArray[2]:
                        for l in lon:
                            lons.append(l)
                        break
                    print(lats)
                    print(len(lats))
                    print(lons)
                    print(len(lons))
                latIndex = 0
                for lat in lats:
                    lonIndex = 0
                    for lon in lons:
                        if (lat, lon) not in position:
                            position[(lat, lon)] = {}
                        if level not in position[(lat, lon)]:
                            position[(lat, lon)][level] = Level(level, typeOfLevel)
                        if name not in position[(lat, lon)].get(level).parameters:
                            position[(lat, lon)].get(level).addParameter(
                                Parameter(name, data[latIndex][lonIndex], unit))
                        lonIndex += 1
                    latIndex += 1
    print("finished")

                #json_content["message "+tmp[0]] = json_param
       # my_json.write(json.dumps(content, cls=NumpyEncoder))


if __name__ == '__main__':
    extract()
