import pygrib as grib
import struct
import numpy as np
import csv
import json


def convertToCSV():
    file = 'gfs.t00z.pgrb2.0p25.f003'  # example filename
    coordinate1 = (47.66033, 9.17582)
    coordinate2 = (48.137154, 11.576124)
    dataParamsToExtract = ["wind", "pressure", "height"]
    latlons = []
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
    json_content = {}
    with open(json_name + ".json", "w+") as my_json:
        for lines in f:
            json_param = {}
            tmp = str(lines).split(':')[:2]
            if any(dataParamToExtract in tmp[1].lower() for dataParamToExtract in dataParamsToExtract):
                print(tmp)
                g = f[int(tmp[0])]
                typeOfLevel = g.typeOfLevel
                level = g.level
                name = g.name
                dataArray = g.data(coordinate1[0], coordinate2[0], coordinate1[1], coordinate2[1])
                data = []
                unit = g.parameterUnits
                for k in dataArray:
                        for l in k:
                           data.append(l)
                if len(latlons) == 0:
                    latlons = data[2:]
                    data = data[:2]
                    json_param["latlons"] = latlons
                    json_param["nameLevel"] = typeOfLevel
                    json_param["nrLevel"] = level
                    json_param["paramName"] = name
                    json_param["paramUnit"] = unit
                    json_param["paramData"] = data
                else:
                    data = data[:2]
                    json_param["nameLevel"] = typeOfLevel
                    json_param["nrLevel"] = level
                    json_param["paramName"] = name
                    json_param["paramUnit"] = unit
                    json_param["paramData"] = data
                json_content["message "+tmp[0]] = json_param
        my_json.write(json.dumps(json_content, cls=NumpyEncoder))

if __name__ == '__main__':
    convertToCSV()
