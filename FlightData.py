class FlightData:
    def __init__(self, file_name_simulation):
        self.file_name = file_name_simulation
        self.entry_list = {}
        file = open(file_name_simulation, "r")
        file.readline()  # skip header
        file.readline()

        for line in file:
            values = line.split('\t')
            self.entry_list[int(values[0])] = Entry(values[1], values[2], values[3], values[4], values[5], values[6],
                                                    values[7],
                                                    values[8], values[9], values[10], values[11], values[12],
                                                    values[13],
                                                    values[14],
                                                    values[15], values[16], values[17], values[18], values[19],
                                                    values[20],
                                                    values[21],
                                                    values[22], values[23])

    def __repr__(self):
        return str(self.entry_list)

    def get_waypoints(self):
        return {k: v for (k, v) in self.entry_list.items() if v.is_wp is True}

    def get_path_filtered(self, num_points):
        step_size = len(self.entry_list) / num_points
        key_index = 1
        path_filtered = []

        for _ in range(1, num_points + 1):
            path_filtered.append(self.entry_list[round(key_index)])
            key_index = key_index + step_size

        return path_filtered

    def get_sections_filtered(self, num_points):
        wps = list(self.get_waypoints().keys())

        sections_filtered = []

        for i in range(0, len(wps) - 1):
            section = {k: v for (k, v) in self.entry_list.items() if k in range(wps[i], wps[i + 1])}
            step_size = len(section) / num_points

            key_index = list(section.keys())[0]
            section_filtered = []

            for _ in range(1, num_points + 1):
                section_filtered.append(section[round(key_index)])
                key_index = key_index + step_size

            sections_filtered.append(section_filtered)

        return sections_filtered

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


class Entry:
    """
        Attributes:
            time_stamp (str): DateTime. TimeStamp of entry.
            is_wp (bool): True if position reached waypoint.
            altitude (float): ft. Current attitude.
            true_track (float): °. ?.
            magnetic_track (float): °. ?
            wind_angle (float): °. ?
            wind_speed (float): kt. ?
            head_wind_indic (?): unit?.
            cross_wind_indic (?): unit?
            tail_wind_comp (float): kt. ?
            cross_wind_comp_abs (float): kt ?
            true_heading (float): °. ?.
            magnetic_heading (float): °. ?
            wca (float): °. ?.
            eas (float): kt. ?.
            tas (float): kt. ?.
            gs (float): kt. ?.
            gc_dist_to_next_wp (float): NM. ?.
            gc_dist_to_destination_through_wp (float): NM. ?.
            navi_time_to_next_wp (str): time. ?.
            flight_time (str): time. ?.
            latitude (float): °. Latitude.
            longitude (float): °. Longitude.
        """

    def __init__(self, timestamp, is_wp, attitude, true_track, magnetic_track, wind_angle, wind_speed, head_wind_indic,
                 cross_wind_indic, tail_wind_comp, cross_wind_comp_abs, true_heading, magnetic_heading, wca, eas, tas,
                 gs,
                 gc_dist_to_next_wp,
                 gc_dist_to_destination_through_wp, navi_time_to_next_wp, flight_time, latitude, longitude):
        self.time_stamp = timestamp
        self.is_wp = is_wp is not ''
        self.attitude = float(attitude) if attitude else None
        self.true_track = float(true_track) if true_track else None
        self.magnetic_track = float(magnetic_track) if magnetic_track else None
        self.wind_angle = float(wind_angle) if wind_angle else None
        self.wind_speed = float(wind_speed) if wind_speed else None
        self.head_wind_indic = float(head_wind_indic) if head_wind_indic else None
        self.cross_wind_indic = float(cross_wind_indic) if cross_wind_indic else None
        self.tail_wind_comp = float(tail_wind_comp) if tail_wind_comp else None
        self.cross_wind_comp_abs = float(cross_wind_comp_abs) if cross_wind_comp_abs else None
        self.true_heading = float(true_heading) if true_heading else None
        self.magnetic_heading = float(magnetic_heading) if magnetic_heading else None
        self.wca = float(wca) if wca else None
        self.eas = float(eas) if eas else None
        self.tas = float(tas) if tas else None
        self.gs = float(gs) if gs else None
        self.gc_dist_to_next_wp = float(gc_dist_to_next_wp) if gc_dist_to_next_wp else None
        self.gc_dist_to_destination_through_wp = float(
            gc_dist_to_destination_through_wp) if gc_dist_to_destination_through_wp else None
        self.navi_time_to_next_wp = navi_time_to_next_wp
        self.flight_time = flight_time
        self.latitude = float(latitude) if latitude else None
        self.longitude = float(longitude) if longitude else None

    def __repr__(self):
        return 'Entry ' + str(self.__dict__)
