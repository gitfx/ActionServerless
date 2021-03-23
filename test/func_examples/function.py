import json
# import but not used, just for testing package installation
import openpyxl

# GET /test/result/python.json

greeting = {"hello": "world"}
print(json.dumps(greeting))

# GET /test/result/python_second.json

print(json.dumps(greeting))

# GET /test/result/python_string

print("hello world")
