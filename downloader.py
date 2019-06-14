import datetime
import ftplib
import os
import FlightData


def download(start, end):
    while start <= end:
        local_path = 'grib2_files/' + start.strftime('%Y-%m-%d')
        os.makedirs(local_path, exist_ok=True)
        download_file(start, local_path)
        start += datetime.timedelta(hours=6)


def download_file(time_stamp, local_path):
    path = '/pub/data/nccf/com/gfs/prod/gfs.' + time_stamp.strftime('%Y') + time_stamp.strftime(
        '%m') + time_stamp.strftime('%d') + time_stamp.strftime('%H') + '/'

    files = {'gfs.t' + time_stamp.strftime('%H') + 'z.pgrb2.0p25.f003',
             'gfs.t' + time_stamp.strftime('%H') + 'z.pgrb2.0p25.f006'}

    for file in files:
        print(path + file)

        # only download if file doesn't exist
        try:
            open(local_path + '/' + file, 'r')
            print('file exists')
        except FileNotFoundError:
            print('Starting download')
            ftp = ftplib.FTP('ftp.ncep.noaa.gov')
            ftp.login()
            ftp.cwd(path)
            ftp.retrbinary('RETR ' + file, open(local_path + '/' + file, 'wb').write, 1024)
            ftp.quit()
            print('downloaded: ' + file)


if __name__ == '__main__':
    flight_data = FlightData.FlightData('2019-05-01_EDDM-EDDH_Aviator.tsv')
    tmp_list = list(flight_data.entry_list.values())
    first_ts = tmp_list[0].get_timestamp_of_section()
    last_ts = tmp_list[len(tmp_list) - 1].get_timestamp_of_section()
    download(first_ts, last_ts)
