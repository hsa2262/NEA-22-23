import json

data = {
    "tvrehubv": "vfiebvfs"
}

with open("save_file.json", "w") as save_file:
    json.dump(data, save_file)


with open("save_file.json") as save_file:
    data = json.load(save_file)
    for i in data.items():
        print(i)

