import requests
from population import Population

key = "" # your key
class Position:

    def __init__(self, longitude, latitude):

        self.req = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="
                           + str(longitude) + "," + str(latitude) +
                           "&key=" + key)

position = Position(23.482895244452575, 120.45804793147344)
p = position.req
json = p.json()
result = json['results']
s = ''
for l in result:
    if l['formatted_address'][-1] == '里' or l['formatted_address'][-1] == '村':
        s = l['formatted_address'].split(", ")[2]
        s.replace("臺", "台")
        print(l['formatted_address'].split(", ")[2])

pop = Population()
print(pop.d[s])

