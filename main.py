from population import Population
from village import Village
from compute import list_add
p = Population()
v = Village()


def multiply_population_data(population_data, proportion):
    population_data["household_no"] *= proportion
    population_data["people_total"] *= proportion
    population_data["people_total_m"] *= proportion
    population_data["people_total_f"] *= proportion
    population_data["people_m"] = [t*proportion for t in population_data["people_m"]]
    population_data["people_f"] = [t*proportion for t in population_data["people_f"]]
    return population_data

def add_population_data(population_data1, population_data2):
    if population_data1 == {}:
        return population_data2
    else:
        population_data1["household_no"] += population_data2["household_no"]
        population_data1["people_total"] += population_data2["people_total"]
        population_data1["people_total_m"] += population_data2["people_total_m"]
        population_data1["people_total_f"] += population_data2["people_total_f"]
        population_data1["people_m"] = list_add(population_data1["people_m"], population_data2["people_m"])
        population_data1["people_f"] = list_add(population_data1["people_f"], population_data2["people_f"])
        return population_data1

def get_villages_name_and_proportion(latitude, longitude, radius):
    villages = v.find_cross_villages(latitude=latitude, longitude=longitude, radius=radius)
    result = []
    for village in villages:
        proportion = v.find_proportion(village, latitude, longitude, radius)
        result.append((village[2], proportion))

    return result

def get_population(latitude, longitude, radius):

    villages = get_villages_name_and_proportion(latitude, longitude, radius)
    print(villages)
    population_data = {}
    for n_p in villages:
        name = n_p[0]
        proportion = n_p[1]
        new_population_data = multiply_population_data(p.d[name], proportion)
        population_data = add_population_data(population_data, new_population_data)

    carry(population_data)
    return population_data

def carry(population_data):


    population_data["people_total_m"] = int(0.5 + population_data["people_total_m"])
    population_data["people_total_f"] = int(0.5 + population_data["people_total_f"])
    population_data["household_no"] = int(population_data["household_no"] + 0.5)
    population_data["people_total"] = int(0.5 + population_data["people_total"])

    population_data["people_m"] = [int(t + 0.5) for t in population_data["people_m"]]
    population_data["people_f"] = [int(t + 0.5) for t in population_data["people_f"]]
    return population_data

print(get_population(24.976340, 121.280176, 500))