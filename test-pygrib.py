import pygrib as grib
import struct
import numpy


def test():
  file = 'gfs.t00z.pgrb2.0p25.f003' #example filename
  grbindx = grib.index(file, 'shortName', 'typeOfLevel', 'level')
  print(grbindx.keys)
  f= grib.open(file)


  for g in f:
      print (g.keys())




if __name__ == '__main__':
    test()
