import os
import csv


class Population:

    def add_to_dict(self, row: list):
        village = row[2] + row[3]
        self.d[village] = self.row2dict(row)

    @staticmethod
    def row2dict(row: list):
        d = dict()
        d["household_no"] = row[4]
        d["people_total"] = row[5]
        d["people_total_m"] = row[6]
        d["people_total_f"] = row[7]
        d["people_m"] = row[8:][::2]
        d["people_f"] = row[9:][::2]
        return d

    def __init__(self):
        self.d = dict()
        with open(os.path.join('data', 'population.csv'), mode='r', newline='') as csv_file:

            rows = csv.reader(csv_file)
            print(type(rows))
            rows = list(rows)
            rows[0][0] = 'statistic_yyymm'
            row_len = len(rows)

            # replace 全形空白
            for x in range(2, row_len):
                rows[x][1] = rows[x][1].replace(" ", "")
                rows[x][1] = rows[x][1].replace("臺", "台")
                rows[x][2] = rows[x][2].replace("臺", "台")
                if "\u3000" in rows[x][2]:
                    rows[x][2] = rows[x][2].replace("\u3000", "")
                self.add_to_dict(rows[x])
