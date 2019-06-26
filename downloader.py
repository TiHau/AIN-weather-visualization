import datetime
import ftplib
import os


def download(start, end):
    """downloads all files from start -6 hours to end +6 hours

            Args:
                    start (datetime): first timestamp of simulation.
                    end (datetime): last timestamp of simulation.
                       """
    start -= datetime.timedelta(hours=6)
    while start <= end:
        local_path = 'grib2_files/' + start.strftime('%Y-%m-%d')
        os.makedirs(local_path, exist_ok=True)
        download_file(start, local_path)
        start += datetime.timedelta(hours=6)


def download_file(time_stamp, local_path):
    """downloads relevant files for time_Stamp
            Args:
                    time_stamp (datetime): Requested timestamp.
                    local_path (str): Where to save that files. (Relative path)
                    """
    path = '/pub/data/nccf/com/gfs/prod/gfs.' + time_stamp.strftime('%Y') + time_stamp.strftime(
        '%m') + time_stamp.strftime('%d') + "/" + time_stamp.strftime('%H') + '/'

    files = {'gfs.t' + time_stamp.strftime('%H') + 'z.pgrb2.0p25.f003',
             'gfs.t' + time_stamp.strftime('%H') + 'z.pgrb2.0p25.f006'}

    for file in files:
        print(path + file)
        # only download if file doesn't exist
        try:
            open(local_path + '/' + file, 'r')
            print('File exists')
        except FileNotFoundError:
            print('Starting download')
            ftp = ftplib.FTP('ftp.ncep.noaa.gov')
            ftp.login()
            ftp.cwd(path)
            ftp.retrbinary('RETR ' + file, open(local_path + '/' + file, 'wb').write, 1024)
            ftp.quit()
            print('downloaded: ' + file)
