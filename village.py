import os
import csv
import requests
from math import pi, sqrt
from compute import get_area
_url = "https://sheethub.com/data.gov.tw/%E5%85%A8%E5%8F%B0%E7%81%A3%E6%9D%91%E9%87%8C%E7%95%8C%E5%9C%96_20140501/uri/"
_format = "?format=geojson"

class Village:

    def __init__(self):
        self.villages = []
        self.read_file()
        # print(self.find_cross_villages(24.76270664, 121.75545391, 300))
        # print(len(self.find_cross_villages(24.76270664, 121.75545391, 300)))
        # for village in self.find_cross_villages(24.76270664, 121.75545391, 300):
            # print(self.find_proportion(village, 24.76270664, 121.75545391, 300))
    def la_lo_radius(self, village):
        return [village[1], village[0], village[-1]]

    def find_proportion(self, village, latitude, longitude, radius):
        la_lo_radius = self.la_lo_radius(village)
        la_lo_radius[0] *=  110758.2
        latitude_in_meter = latitude * 110758.2
        la_lo_radius[1] *= 101751.8
        longitude_in_meter = longitude * 101751.8
        area = get_area(x1=la_lo_radius[0], y1=la_lo_radius[1],
                        x2=latitude_in_meter, y2=longitude_in_meter,
                        r1=la_lo_radius[2], r2=radius)
        return area / village[-2]

    def find_cross_villages(self, latitude, longitude, radius):
        cross_villages = []
        for village in self.villages:
            longitude_diff = longitude - village[0]
            latitude_diff = latitude - village[1]
            max_length = radius + village[-1]
            if ((longitude_diff * 101751.8)**2 + (latitude_diff *110758.2)**2) < max_length**2:
                cross_villages.append(village)
        return cross_villages

    def read_file(self):
        with open(os.path.join("data", "village2.csv"), mode='r', newline="") as csv_file:
            rows = csv.reader(csv_file)

            rows = list(rows)
            for i in range(len(rows)):
                rows[i] = [float(rows[i][4]), float(rows[i][5]),
                           rows[i][1] + rows[i][2] + rows[i][3],
                           float(rows[i][6]), float(rows[i][7])]
            self.villages = rows
        print(self.villages)

    # 升格處理
    def correct(self, row):
        for j in range(2, 5):
            row[j] = self.correct_tai(row[j])
        if row[4] == "桃園縣":
            row[4] = "桃園市"
            row[3] = row[3][:-1] + "區"
            row[2] = row[2][:-1] + "里"
        return row

    def correct_tai(self, str_):
        return str_.replace("臺", "台")

    def get_centroid(self, dl):

        latitude = 0  # 經度
        longitude = 0  # 緯度
        for l in dl:
            latitude += l[0]
            longitude += l[1]

        latitude /= len(dl)
        longitude /= len(dl)
        return [latitude, longitude]

    def get_area(self, dl):
        area = 0.0
        dc = dl[:]
        for i in range(len(dl)):
            dc[i][0] = dl[i][0] *  101751.8
            dc[i][1] = dl[i][1] *  110758.2
        for i in range(len(dc) - 1):
            area += dc[i][0] * dc[i+1][1]
            area -= dc[i][1] * dc[i + 1][0]
        area /= 2
        return abs(area)

    def write_file(self):
        f = open(os.path.join("data", "village2.csv"), 'a')
        with open(os.path.join("data", "village.csv"), mode='r', newline="") as csv_file:
            rows = csv.reader(csv_file)
            print(type(rows))
            rows = list(rows)
            row_len = len(rows)
            for i in range(1, row_len):
                rows[i] = self.correct(rows[i])
                area = rows[i][-1]
                rows[i] = [rows[i][0], rows[i][4], rows[i][3], rows[i][2]]
                print(rows[i])

                dl = requests.get(_url + rows[i][0] + _format).json()['features'][0]['geometry']['coordinates'][0]

                if len(dl) == 1:
                    centroid = self.get_centroid(dl[0])
                else:
                    centroid = self.get_centroid(dl)

                radius = sqrt(float(area) / pi)


                rows[i].extend(centroid)
                rows[i].append(area)
                rows[i].append(radius)


                print(rows[i])
                for item in rows[i]:
                    if type(item) == type(""):
                        f.write(item + ',')
                    else:
                        f.write(str(item) + ",")
                f.write('\n')
        f.close()
Village()