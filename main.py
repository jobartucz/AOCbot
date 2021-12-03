### individual:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
# cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
### team:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/1566841.json'
# cookies = dict(session='53616c7465645f5fc012ab039fb15a6fa623b7dca5a054d92e41ad9e667462260622bee83ecb5892e12d22b4b7aa579b')
### college:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/1567131.json'
# cookies = dict(session='53616c7465645f5f6af580b520db3b7acaa0d4a0f305ef5188fa1e2e4f8e0b2ff13c15bd22f17fb790eb64602b09311c')


import requests
import json
import csv
import os
import time
import socket
from random import randint

host = socket.gethostname() # for outputting html
if host == "saturn":
    print('<!DOCTYPE html><html><head><title>RCC Winter Programming Competition 2021</title>')
    print('<link rel="stylesheet" href="stylesheets/styles.css">')
    print('<meta http-equiv="refresh" content="60" ><meta charset="UTF-8">')
    print('</head><body class="container">')
    print('<h1 class="rainbow">RAYTF & RCC Winter Programming Competition 2021 Leader-board</h1>')
    print(f"Updated at: {time.asctime()}\n")
    print("<p id='clock'></p>")

# print(time.time() - os.path.getmtime("data_file.json"))
# print(time.time(), os.path.getmtime("data_file.json"))
usefile = False # get fresh data
# if it's been less than 15 minutes, just use what we had before.
filepath = "./"
if host == "saturn":
    filepath = "/var/www/html/python/AOCbot/"
if time.time() - os.path.getmtime(filepath + "data_file.json") < 500:
    usefile = True
else:
    print(f"Getting fresh data {time.time() - os.path.getmtime(filepath + 'data_file.json')}")

users = {}
schools = {}
teams = {}
userfile = filepath + 'users.csv'
with open(userfile, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        # print(' *** '.join(row))
        users[row[5]] = row[2]
        schools[row[5]] = row[4]
        if row[7] == "Team":
            teams[row[5]] = row[8]

schoolstars = {}
numparticipants = {}
teamstars = {}


if host == "saturn":
    print("\n<div id='individuals'>\n")
    print("\n<h2>Individuals:</h2><ol>\n")
else:
    print("\nIndividuals with at least one star:\n")

if (usefile == True):
    with open(filepath + "data_file.json", "r") as read_file:
        data = json.loads(json.load(read_file))
else:
    url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
    cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
    r = requests.get(url, cookies=cookies)
    # print(r.text)
    data = json.loads(r.text)

    with open(filepath + "data_file.json", "w") as write_file:
        json.dump(r.text, write_file)

starlist = []
for m in data["members"]:
    if data['members'][m]['stars']:
        #print(m)
        #print(data["members"][m])
        starlist.append(data["members"][m])

# resort the list by number of stars then local-score (reversed)
starlist = sorted(starlist, key = lambda starlist: (starlist['stars'], starlist['local_score']),reverse=True)
for entry in starlist:
    if entry['name'] in teams:
        continue # don't double-count team members!
    if entry['name'] in users:
        if host == "saturn":
            print(f"<li><span class='{schools[entry['name']]}'>")
        print(f"{users[entry['name']]} ({schools[entry['name']]}): {entry['stars']} stars")
        if host == "saturn":
            print("</span></li>")

        if schools[entry['name']] in schoolstars:
            schoolstars[schools[entry['name']]] += entry['stars']
            numparticipants[schools[entry['name']]] += 1
        else:
            schoolstars[schools[entry['name']]] = entry['stars']
            numparticipants[schools[entry['name']]] = 1
        
        schoolstars['CTECH'] = randint(-2000, 2000) * 0.5
        numparticipants['CTECH'] = 1

    else:
        if host == "saturn":
            pass
            # print("<li>")
            # print(f"{entry['name']} not registered - not counted: {entry['stars']} stars - go here to fix: <a href='https://forms.gle/kjF6wU71oXkJUaMD9'>https://forms.gle/kjF6wU71oXkJUaMD9</a>")
            # print("</li>")
        else:
            print(f"{entry['name']} not registered - not counted: {entry['stars']} stars")


if host == "saturn":
    print("\n</ol>\n")
    print("If your name is on the AOC board, but not here, you probably didn't fill out the Google Form, or typed in your AOC username incorrectly.<br>\n")
    print("You can go here to fix it: <a href='https://forms.gle/kjF6wU71oXkJUaMD9'>https://forms.gle/kjF6wU71oXkJUaMD9</a>")
    print("</li>")
    print("</div>\n")
    print("\n<div id='teams'>\n")
    print("<h2>Teams:</h2>\n<ol>\n")
else:
    print("\nTeams:\n")

if (usefile == True):
    with open(filepath + "team_file.json", "r") as read_file:
        data = json.loads(json.load(read_file))
else:
    url = 'https://adventofcode.com/2021/leaderboard/private/view/1566841.json'
    cookies = dict(session='53616c7465645f5fc012ab039fb15a6fa623b7dca5a054d92e41ad9e667462260622bee83ecb5892e12d22b4b7aa579b')
    r = requests.get(url, cookies=cookies)
    # print(r.text)
    data = json.loads(r.text)

    with open(filepath + "team_file.json", "w") as write_file:
        json.dump(r.text, write_file)

# create the list of users and their stars
starlist = []
for m in data["members"]:
    if data['members'][m]['stars']:
        #print(m)
        #print(data["members"][m])
        starlist.append(data["members"][m])

# resort the list by number of stars (reversed)
starlist = sorted(starlist, key = lambda starlist: starlist['local_score'],reverse=True)
for entry in starlist:
    if entry['name'] in users:
        if entry['name'] not in teams: # individual joined the team leaderboard
            continue
        if teams[entry['name']] in teamstars:
            # print(f"skipping {users[entry['name']]}, already got {teams[entry['name']]} stars from other member")
            continue # skip teams that already have a higher entry
        else:
            # print(f"{teams[entry['name']]} : {entry['stars']} stars")
            teamstars[teams[entry['name']]] = entry['stars']

            if teams[entry['name']] == "Ctrl Alt Defeat":
                schoolstars["Mayo"] += entry['stars']
                numparticipants["Mayo"] += 1
                print(f"<li class='Mayo'>Ctrl Alt Defeat (Mayo/Mayo): {entry['stars']} stars</li>")
            elif teams[entry['name']] == "CODINGBEASTS":
                schoolstars["Mayo"] += entry['stars']
                numparticipants["Mayo"] += 1
                print(f"<li class='Mayo'>CODINGBEASTS (Mayo/Mayo): {entry['stars']} stars</li>")
            elif teams[entry['name']] == "Null Programmers Exception":
                schoolstars["Mayo"] += (entry['stars'] * 1) / 2.0
                schoolstars["Century"] += (entry['stars'] * 1) / 2.0
                numparticipants["Mayo"] += 0.5
                numparticipants["Century"] += 0.5
                print(f"<li style='color:#00CCCC'>Null Programmers Exception (Century/Mayo): {entry['stars']} stars</li>")


    else:
        print(f"ERROR!!! {entry['name']} : {entry['stars']} stars")



if host == "saturn":
    print("\n</ol>\n</div>\n")
    print("\n<div id='schools'>\n")
    print("\n<h2>Schools:</h2>\n<ol>\n")
else:
    print("\nSchools:\n")

        
schoolstars = {k: v for k, v in sorted(schoolstars.items(), key=lambda item: item[1], reverse=True)}

for k in schoolstars:
    if host == "saturn":
        print(f"<li><span class='{k}'>")

    print(f"{k} : {schoolstars[k]:.1f} total stars, {numparticipants[k]:.1f} participants, {schoolstars[k] / numparticipants[k]:.1f} efficiency rating")
    if host == "saturn":
        print("</span></li>")

if host == "saturn":
    print("</ol>")
    print("\n</div>\n")
    print("\n</html></body>")
