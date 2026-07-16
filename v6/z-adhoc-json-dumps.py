import json


dict_data = {"a": 1, "b": 2}

print(dict_data)

json_str = json.dumps(dict_data)

print("-" * 20)
print(type(json_str))
print(json_str)
