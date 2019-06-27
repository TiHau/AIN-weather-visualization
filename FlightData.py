import datetime


class FlightData:
    def __init__(self, file_name_simulation):
        self.file_name = file_name_simulation
        self.entry_list = {}
        file = open(file_name_simulation, "r")
        file.readline()  # skip header
        file.readline()

        for line in file:
            values = line.split('\t')
            ts = values[1].split('.')[0]  # cut millis
            ts = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
            self.entry_list[int(values[0])] = Entry(ts, values[2], values[3], values[22], values[23])

    def __repr__(self):
        return str(self.entry_list)

    def get_path_filtered(self, num_points):
        """
        Splits the list into a number of entry's
        :param num_points: The Number of entry's
        :return:
        """
        step_size = len(self.entry_list) / num_points
        key_index = 1
        path_filtered = []

        for _ in range(1, num_points + 1):
            path_filtered.append(self.entry_list[round(key_index)])
            key_index = key_index + step_size

        return path_filtered

    def get_min_latitude(self):
        tmp = []
        for entry in self.entry_list.values():
            tmp.append(entry.latitude)
        return min(tmp)

    def get_max_latitude(self):
        tmp = []
        for entry in self.entry_list.values():
            tmp.append(entry.latitude)
        return max(tmp)

    def get_min_longitude(self):
        tmp = []
        for entry in self.entry_list.values():
            tmp.append(entry.longitude)
        return min(tmp)

    def get_max_longitude(self):
        tmp = []
        for entry in self.entry_list.values():
            tmp.append(entry.longitude)
        return max(tmp)

    def split_in_timesections(self):
        """
        Returns a list of datetime's in 3 hour intervals
        :return: Datetime
        """
        res = []

        tmp_list = list(self.entry_list.copy().values())
        tmp_list.reverse()

        while len(tmp_list) > 0:
            entry = tmp_list.pop()
            ts = entry.get_timestamp_of_section()

            if ts not in res:
                res.append(ts)

        res.append(ts+datetime.timedelta(hours=3))

        return res


class Entry:
    """
        Attributes:
            timestamp (datetime): DateTime. TimeStamp of entry.
            is_wp (bool): True if position reached waypoint.
            attitude (float): ft. Current attitude.
            latitude (float): °. Latitude.
            longitude (float): °. Longitude.
        """

    def __init__(self, timestamp, is_wp, attitude, latitude, longitude):
        self.timestamp = timestamp
        self.is_wp = is_wp is not ''
        self.attitude = float(attitude) if attitude else None
        self.latitude = float(latitude) if latitude else None
        self.longitude = float(longitude) if longitude else None

    def __repr__(self):
        return 'Entry ' + str(self.__dict__)

    def get_timestamp_of_section(self):
        """
        Round off the time stamp for the next eighth hour
        :return: DateTime
        """
        ts = self.timestamp
        if ts.hour in {0, 1, 2}:
            tmp_hour = 0
        elif ts.hour in {3, 4, 5}:
            tmp_hour = 3
        elif ts.hour in {6, 7, 8}:
            tmp_hour = 6
        elif ts.hour in {9, 10, 11}:
            tmp_hour = 9
        elif ts.hour in {12, 13, 14}:
            tmp_hour = 12
        elif ts.hour in {15, 16, 17}:
            tmp_hour = 15
        elif ts.hour in {18, 19, 20}:
            tmp_hour = 18
        else:
            tmp_hour = 21
        ts = ts.replace(microsecond=0, second=0, minute=0, hour=tmp_hour)
        return ts
