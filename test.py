import json

with open("output/test-3.json", "r") as f:
    data = json.load(f)

print(len(data))