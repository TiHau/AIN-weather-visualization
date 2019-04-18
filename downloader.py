import ftplib


def download():
    ftp = ftplib.FTP('ftp.ncep.noaa.gov')

    ftp.login()

    ftp.cwd('/pub/data/nccf/com/gfs/prod/gfs.2019040812/')

    file = "gfs.t12z.pgrb2.0p25.f003"  # example filename

    ftp.retrbinary('RETR ' + file, open(file, 'wb').write, 1024)

    ftp.quit()

    return file
