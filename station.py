import numpy
import math

# Effects: Returns Correlation coefficient of 2 arrays of data, ignores nan values
def correlation(set1, set2):  # inputs are individual sets i.e. dBN, dBE
    count1 = 0
    count2 = 0
    for value1, value2 in zip(set1, set2):
        if not numpy.isnan(value1):
            count1 += 1
        if not numpy.isnan(value2):
            count2 += 1
    mean1 = numpy.nansum(set1) / count1
    mean2 = numpy.nansum(set2) / count2
    numerator = 0
    for value1, value2 in zip(set1, set2):
        if not numpy.isnan(value1) and not numpy.isnan(value2):
            numerator += ((value1 - mean1) * (value2 - mean2))
    deviation_1 = 0
    deviation_2 = 0
    for value1, value2 in zip(set1, set2):
        if not numpy.isnan(value1) and not numpy.isnan(value2):
            deviation_1 += (value1 - mean1) ** 2
            deviation_2 += (value2 - mean2) ** 2
    denominator = math.sqrt(deviation_1 * deviation_2)
    return numerator / denominator


class Station:
    mag_long = 0
    mag_lat = 0
    db_north = []
    db_east = []
    db_vertical = []
    db_horizontal = []

    def __init__(self, data, station_num):
        self.mag_long = data['mlon'][1:station_num]
        self.mag_lat = data['mlat'][1:station_num]
        self.db_north = data['dbn_geo'][:, station_num]
        self.db_east = data['dbe_geo'][:, station_num]
        self.db_vertical = data['dbz_geo'][:, station_num]
        self.db_horizontal = self.create_horizontal_vector()

    # Effects: Returns an array of 2 lists that hold the magnitude and direction of magnetic field vectors of the data set
    def create_horizontal_vector(self):
        magnitude = []
        direction = []
        for north, east in zip(self.db_north, self.db_east):
            if numpy.isnan(north) or numpy.isnan(north):
                magnitude.append(numpy.nan)
                direction.append(numpy.nan)
            else:
                current_mag = math.sqrt(north ** 2 + east ** 2)
                magnitude.append(current_mag)
                current_dir = math.atan(north / east)
                direction.append(current_dir)
        horizontal = [magnitude, direction]
        return horizontal

    # Requires: 2 Initialized station objects
    # Effects: Returns correlation of magnitude and direction of the 2 stations
    def vector_correlation(self, other_station):
        mag_correlation = correlation(self.db_horizontal[0], other_station.db_horizontal[0])
        dir_correlation = correlation(self.db_horizontal[1], other_station.db_horizontal[1])
        return [mag_correlation, dir_correlation]

    # Requires: 2 Initialized station objects
    # Effects Returns distance calculated between the 2 stations
    def find_distance(self, other_station):
        lat_1 = self.mag_lat * math.pi / 180
        long_1 = self.mag_long * math.pi / 180
        lat_2 = other_station.mag_lat * math.pi / 180
        long_2 = other_station.mag_long * math.pi / 180
        distance = 6377.83 * math.acos((math.sin(lat_1) * math.sin(lat_2)) +
                                       math.cos(lat_1) * math.cos(lat_2) * math.cos(long_2 - long_1))
        return distance
