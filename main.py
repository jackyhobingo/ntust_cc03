from population import Population
from village import Village
from compute import list_add
from flask import Flask, request, render_template, Blueprint, send_from_directory
from config import DevConfig
import json
from jinja2 import Template

profile = Blueprint('opendata_final', __name__)

p = Population()
v = Village()


def multiply_population_data(population_data, proportion):
    result = dict()
    result["household_no"] = population_data["household_no"] * proportion
    result["people_total"] = population_data["people_total"] * proportion
    result["people_total_m"] = population_data["people_total_m"] * proportion
    result["people_total_f"] = population_data["people_total_f"] * proportion
    result["people_m"] = [t*proportion for t in population_data["people_m"]]
    result["people_f"] = [t*proportion for t in population_data["people_f"]]
    return result

def add_population_data(population_data1, population_data2):
    if population_data1 == {}:
        return population_data2
    else:
        result = dict()
        result["household_no"] = population_data1["household_no"] + population_data2["household_no"]
        result["people_total"] = population_data1["people_total"] + population_data2["people_total"]
        result["people_total_m"] = population_data1["people_total_m"] + population_data2["people_total_m"]
        result["people_total_f"] = population_data1["people_total_f"] + population_data2["people_total_f"]
        result["people_m"] = list_add(population_data1["people_m"], population_data2["people_m"])
        result["people_f"] = list_add(population_data1["people_f"], population_data2["people_f"])
        return result

def get_villages_name_and_proportion(latitude, longitude, radius):
    villages = v.find_cross_villages(latitude=latitude, longitude=longitude, radius=radius)
    result = []
    for village in villages:
        proportion = v.find_proportion(village, latitude, longitude, radius)
        result.append((village[2], proportion))

    return result

def get_population(latitude, longitude, radius):

    villages = get_villages_name_and_proportion(latitude, longitude, radius)
    # print(villages)
    population_data = dict()
    for n_p in villages:
        name = n_p[0]
        proportion = n_p[1]
        new_population_data = multiply_population_data(p.d[name], proportion)
        population_data = add_population_data(population_data, new_population_data)


    return carry(population_data)

def carry(population_data):
    result = dict()
    result["people_total_m"] = int(0.5 + population_data["people_total_m"])
    result["people_total_f"] = int(0.5 + population_data["people_total_f"])
    result["household_no"] = int(population_data["household_no"] + 0.5)
    result["people_total"] = int(0.5 + population_data["people_total"])

    result["people_m"] = [int(t + 0.5) for t in population_data["people_m"]]
    result["people_f"] = [int(t + 0.5) for t in population_data["people_f"]]
    return result


app = Flask(__name__, static_url_path='')
# app.register_blueprint(profile)
# app.config.from_object(DevConfig)
blank = {}
@app.route("/")
def hello():
    try:
        latitude = request.args.get("la")
        longitude = request.args.get("lo")
        radius = request.args.get("r")
        d = get_population(float(latitude), float(longitude), float(radius))
        # print(d)
        return json.dumps(d)
    except:

        return json.dumps(blank)
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/opendata.html')
def opendata():

    try:
        latitude = request.args.get("la")
        longitude = request.args.get("lo")
        radius = request.args.get("r")
        d = get_population(float(latitude), float(longitude), float(radius))
        print(d)
        return json.dumps(d)
    except:

        return render_template("opendata.html")
@app.route('/assets/js/<path:path>')
def send_js(path):
    return send_from_directory('assets/js', path)

@app.route('/assets/css/<path:path>')
def send_css(path):
    return send_from_directory('assets/css', path)
@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)
@app.route('/assets/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('assets/fonts', path)

if __name__ == "__main__":

    blank["household_no"] = 0
    blank["people_total"] = 0
    blank["people_total_m"] = 0
    blank["people_total_f"] = 0
    blank["people_m"] = [0 for t in range(101)]
    blank["people_f"] = [0 for t in range(101)]
    app.run(host="0.0.0.0", port=8080)



