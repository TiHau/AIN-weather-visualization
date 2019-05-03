import pygrib as grib
import struct
import numpy as np
import csv
import json


class Level:
    def __init__(self, level, type):
        self.level = level
        self.type = type
        self.parameters = []

    def addParameter(self, parameter):
        return self.parameters.append(parameter)

    def __repr__(self):
        return str(self.__dict__)


class Parameter:
    def __init__(self, name, data, unit):
        self.name = name
        self.data = data
        self.unit = unit

    def __repr__(self):
        return str(self.__dict__)


def extract():
    file = 'gfs.t00z.pgrb2.0p25.f003'  # example filename
    coordinate1 = (4,1)#(47.66033, 9.17582)
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
    content = {}
    with open(json_name + ".json", "w+") as my_json:
        for lines in f:
            position = {}
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
                for latArrays in dataArray[1]:
                    for lons in dataArray[2]:
                        for lon in lons:
                            if (latArrays[0], lon) not in position:
                                position[(latArrays[0], lon)] = {}

                            if level not in position[(latArrays[0], lon)]:
                                position[(latArrays[0], lon)][level] = Level(level, typeOfLevel)

                            #position[(latArrays[0], lon)].get(level).addParameter(Parameter(name, 0, unit))
                        #print(position[(latArrays[0], lon)].get(level))

                #json_content["message "+tmp[0]] = json_param
       # my_json.write(json.dumps(content, cls=NumpyEncoder))

if __name__ == '__main__':
    extract()
