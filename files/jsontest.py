import json


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def compare_json(json1, json2):
    differences = {}
    for key in json1:
        if key not in json2:
            differences[key] = json1[key]
        elif json1[key] != json2[key]:
            differences[key] = {"json1": json1[key], "json2": json2[key]}
    for key in json2:
        if key not in json1:
            differences[key] = json2[key]
    return differences


def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


file1_path = "files/ocrtd.json"
file2_path = "files/oupd.json"
output_path = "files/differences.json"

json1 = read_json(file1_path)
json2 = read_json(file2_path)

differences = compare_json(json1, json2)

write_json(output_path, differences)
