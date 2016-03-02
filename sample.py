import json

# filename = raw_input('Give a file name to analyze: ')
filename = '201602252025.json' # Change this

file = open(filename)
statuses = []
i = 0
maximum_item = 10000 # the maximum number of items to store

for line in file:
    if i < maximum_item:
        if 'delete' not in line:
            statuses.append(json.loads(line))
            i = i + 1
        else:
            continue
    else:
        break

# do something with the statueses
# 
# 
# 