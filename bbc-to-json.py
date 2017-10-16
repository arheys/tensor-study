import json
import os
import glob


path = 'bbc2'
dirs = ['business', 'entertainment', 'politics', 'sport', 'tech']

output = {}
for dir in dirs:
    list = []
    for filename in glob.glob(os.path.join(path + '/' + dir, '*.txt')):
        print(filename)
        f = open(filename)
        text = f.read().replace("\n", " ")
        list.append(text[0:800])
        f.close()
    output[dir] = list



out_file = open("tdata.json", "w")
out_file.write(json.dumps(output))
out_file.close()
