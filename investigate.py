import pickle
from pprint import pprint

with open("merged.pickle", "rb") as handle:
    data = pickle.load(handle)

first_two_letters = {}

for key in data.keys():
    print((key[:2]).lower())
    k = key[:2].lower()
    if k not in first_two_letters:
        first_two_letters[k] = 1
    else:
        first_two_letters[k] += 1

sorted_dict = sorted(first_two_letters.items(), key=lambda kv: kv[1])
most_saturated_10 = sorted_dict[-10:]
pprint(most_saturated_10)

alphabet = 'abcdefghijklmnopqrstuvwxyz'
detailed_list = []
for first_two in most_saturated_10:
    for char in alphabet:
        detailed_list.append(first_two[0] + char)

pprint(detailed_list)
print("length of detailed_list", len(detailed_list))

with open("detailed_list.pickle", 'wb') as handle:
    pickle.dump(detailed_list, handle, protocol=pickle.HIGHEST_PROTOCOL)



