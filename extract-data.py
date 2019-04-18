import pygrib as grib
import struct
import numpy


def test():
    file = 'gfs.t00z.pgrb2.0p25.f003'  # example filename
    coordinate1 = (47.66033, 9.17582)
    coordinate2 = (48.137154, 11.576124)

    f = grib.open(file)

    print(f[5])
    #for g in f:
    g=f[5]
       # print(g)
    csv_name = str(g.typeOfLevel) + "-" + str(g.level) + "-" + str(g.name) + "-data-" + str(g.validDate) + "-" + str( g.analDate) + "-" + str(g.forecastTime)
    import csv

    with open(csv_name + ".csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        for k in g.data(coordinate1[0], coordinate2[0], coordinate1[1], coordinate2[1]):
            for l in k:
                csvWriter.writerow(l)



if __name__ == '__main__':
    test()
