import json

# Function to read and iterate through JSON
def read_and_iterate_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


data = read_and_iterate_json('eventData.json')

for key, value in data.items():
    print(key)

print(len(data))