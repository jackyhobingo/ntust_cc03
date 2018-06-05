import os
import csv
import requests
from math import pi, sqrt

_url = "https://sheethub.com/data.gov.tw/%E5%85%A8%E5%8F%B0%E7%81%A3%E6%9D%91%E9%87%8C%E7%95%8C%E5%9C%96_20140501/uri/"
_format = "?format=geojson"

class Village:

    def __init__(self):
        self.r = []
        self.read_file()

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

    def get_mean_point(self, dl):

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

    def read_file(self):
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
                    mean_point = self.get_mean_point(dl[0])
                else:
                    mean_point = self.get_mean_point(dl)

                radius = sqrt(float(area) / pi)


                rows[i].extend(mean_point)
                rows[i].append(area)
                rows[i].append(radius)

                self.r.append(rows[i])

                print(rows[i])
                for item in rows[i]:
                    if type(item) == type(""):
                        f.write(item + ',')
                    else:
                        f.write(str(item) + ",")
                f.write('\n')
        f.close()