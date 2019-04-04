from bin_structure import BIN
import urllib.request, json, math
import datetime as dt
import numpy as np

# This method form bins from the passed bounding box boundaries and the input bin side.
def form_bins(x_min, x_max, y_min, y_max, bin_side):
    bins = []
    x_size = math.ceil((x_max - x_min)/bin_side)
    y_size = math.ceil((y_max - y_min)/bin_side)
    for i in range(0, y_size):
        y_append_value = min(y_min + i * bin_side, y_max)
        temp = []
        for j in range(0, x_size):
            x_append_value = min(x_min + j * bin_side, x_max)
            temp.append(BIN(x_append_value, y_append_value, bin_size))
        bins.append(temp)
    return bins

# Fetches the list of tracks from the given url.
with urllib.request.urlopen("https://envirocar.org/api/stable/tracks?bbox=7.1,51.1,15.4,65.7&during=2011-11-05T12:00:00Z,2014-11-08T12:00:00Z") as url:
    data = json.loads(url.read().decode())

# Fetches data for individual tracks in the given bounding box and the time frame.
prefix = "https://envirocar.org/api/stable/tracks/"
individual_tracks = []
for tracks in data['tracks']:
    url = prefix + tracks['id']
    with urllib.request.urlopen(url) as repo:
        individual_tracks.append(json.loads(repo.read().decode()))

# Defining a same value of bin size for latitude and longitude, in lat-lng scale. This forms a rectangular bin.
bin_size = 0.5
bins = form_bins(7.1,51.1,15.4,65.7, bin_size)

# This loop puts the speed (demonstrative) data at each timestamp into the respective bin object.
# For simplicity, data has not been aggregated at nearby time intervals.
for tracks in individual_tracks:
    bin_number_y = -1
    bin_number_x = -1
    for points in tracks.get('features'):
        coordinates = points.get('geometry').get('coordinates')
        bin_number_x = math.floor((coordinates[0] - 7.1)/bin_size)
        bin_number_y = math.floor((coordinates[1] - 15.4)/bin_size)
        speed_data = 0
        try: 
            speed_data = points.get('properties').get('phenomenons').get('Speed').get('value')
        except:
            speed_data = np.nan
        date = dt.datetime.strptime(points.get('properties').get('time'), '%Y-%m-%dT%H:%M:%SZ')
        bins[bin_number_y][bin_number_x].set_feature(speed_data, date) 
