import datetime
import ftplib


def download():
    now = datetime.datetime.now()

    if now.hour < 9:
        hour = '00'
    elif now.hour < 13:
        hour = '08'
    elif now.hour < 19:
        hour = '12'
    else:
        hour = '18'

    file = 'gfs.t' + hour + 'z.pgrb2.0p25.f003'
    path = '/pub/data/nccf/com/gfs/prod/gfs.' + str(now.year) + str(now.month) + str(now.day) + hour + '/'

    # only download if file doesn't exist
    try:
        open(file, 'r')
        print('file exists')
    except FileNotFoundError:
        print('Starting download')
        ftp = ftplib.FTP('ftp.ncep.noaa.gov')
        ftp.login()
        ftp.cwd(path)
        ftp.retrbinary('RETR ' + file, open(file, 'wb').write, 1024)
        ftp.quit()
        print('downloaded: ' + file)

    return file


if __name__ == '__main__':
    download()
