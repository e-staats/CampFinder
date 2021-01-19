import json
import pprint
import os

park_vals = []
directory = os.path.join(os.path.dirname(__file__), "..", "json")
for file in os.listdir(directory):
    with open(os.path.join(directory, file)) as json_file:
        data = json.load(json_file)
        for ext_id in data["mapLinkLocalizedValues"]:
            park_vals.append((data["mapLinkLocalizedValues"][ext_id][0]["title"], ext_id))

park_vals.sort()
for name,id in park_vals:
    print(f"{id},{name}")