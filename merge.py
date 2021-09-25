import pickle

with open("fn_scraped.pickle", 'rb') as handle:
    data_fn = pickle.load(handle)

with open("scraped.pickle", "rb") as handle:
    data_ln = pickle.load(handle)

for item in data_fn.keys():
    data_ln[item] = data_fn[item]

with open("merged.pickle", "wb") as handle:
    pickle.dump(data_ln,handle)

