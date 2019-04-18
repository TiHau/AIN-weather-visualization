import pygrib as grib
import struct
import numpy


def test():
    file = 'gfs.t00z.pgrb2.0p25.f003'  # example filename
    coordinate1=(47.66033, 9.17582)
    coordinate2=(48.137154, 11.576124)

    f = grib.open(file)

    print(f[5])
    #for g in f:
    g=f[5]
       # print(g)
    print(g.typeOfLevel, g.level, g.name, g.data(10,20,30,40), g.validDate, g.analDate, g.forecastTime)
    import csv


    with open("new_file.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(g.data(47.66033,48.137154,9.17582,11.576124))

if __name__ == '__main__':
    test()
