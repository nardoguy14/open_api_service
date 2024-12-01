
import json
import sys


json_file = 'stacks.json'

# Load the JSON data from the file
with open(json_file, 'r') as file:
    data = json.load(file)

stacks = data['StackSummaries']

for stack in stacks:
    if stack['StackName'] == sys.argv[1] and stack['StackStatus'] != 'DELETE_COMPLETE':
        print("stack")

print("nostack")
