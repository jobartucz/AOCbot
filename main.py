import requests
import json
import csv

users = {}
with open('users.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        # print(' *** '.join(row))
        users[row[5]] = row[2]

if (True):
    with open("data_file.json", "r") as read_file:
        data = json.loads(json.load(read_file))
else:
    url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
    cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
    r = requests.get(url, cookies=cookies)
    print(r.text)
    data = json.loads(r.text)

    with open("data_file.json", "w") as write_file:
        json.dump(r.text, write_file)

l = []
for m in data["members"]:
    if data['members'][m]['stars']:
        #print(m)
        #print(data["members"][m])
        l.append(data["members"][m])

l = sorted(l, key = lambda l: l['local_score'],reverse=True)
for i in l:
    if i['name'] in users:
        print(f"{users[i['name']]} : {i['stars']}")
    else:
        print(f"{i['name']} : {i['stars']}")
