import pickle
import csv

with open("merged.pickle", 'rb') as handle:
	data = pickle.load(handle)

name_keys = {}

yr_dict = {
    "'25": 0,
    "'24": 0,
    "'23": 0,
    "'22": 0,
    "'21": 0,
    "'20": 0,
    "'19": 0,
    "'18": 0,
    "TH": 0,
    "GREC": 0,
    "GR": 0,
    "GRLS": 0,
    "TU":0,
    "TU25": 0,
    "TU24": 0,
    "TU23": 0,
    "TU22": 0,
    "TU21": 0,
    "TU20": 0,
    "TU19": 0,
    "GRHC": 0,
    "DM": 0,
    "UG": 0,
}

for person in data.keys():
    split = person.split(",")
    name = " ".join(split[:len(split)-1]).strip()
    class_yr = split[-1].strip()

    data[person]["year"] = class_yr
    data[person]["name"] =  name

    if name[:2] not in name_keys:
        name_keys[name[:2]] = 1
    else:
        name_keys[name[:2]] += 1

    try:
        yr_dict[class_yr] += 1
    except:
        pass

print(name_keys)
print(yr_dict)
print(len(data.keys()))

def write_row_to_csv(writer, dat):
    writer.writerow([
        dat["name"],
        dat["year"],
        dat["email"],
        dat["number"],
        dat["mail"],
    ])


with open("final.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for person in data.keys():
        write_row_to_csv(writer, data[person])

with open("final_25.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for person in data.keys():
        if data[person]["year"] == "'25":
            write_row_to_csv(writer, data[person])

with open("final_24.csv", "w", newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for person in data.keys():
        if data[person]["year"] == "'24":
            write_row_to_csv(writer, data[person])
