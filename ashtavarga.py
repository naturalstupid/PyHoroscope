import json
f = open('ashtavarga.json','r')
planets = ['sun','moon','mars','mercury','jupiter','venus','saturn','lagnam']
data = json.load(f)
for t in data:
    print(t)
    