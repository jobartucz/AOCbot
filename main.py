# individual:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
# cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
# team:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/1566841.json'
# cookies = dict(session='53616c7465645f5fc012ab039fb15a6fa623b7dca5a054d92e41ad9e667462260622bee83ecb5892e12d22b4b7aa579b')
# college:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/1567131.json'
# cookies = dict(session='53616c7465645f5f6af580b520db3b7acaa0d4a0f305ef5188fa1e2e4f8e0b2ff13c15bd22f17fb790eb64602b09311c')


import requests
import json
import csv
import os
import time
import socket
from random import choice

mascots = {'Century': choice(['Panthers', 'Panters']), 'JM': choice(['Rockets', 'Rockettes', 'Sprockets']), 'Mayo': choice(
    ['Spartans', 'Sparetires']), 'Kellogg': choice(['Comets', 'Cornflakes']), 'Lincoln': choice(['Logs', 'Lynx'])}
mascots = {'Century': 'Panthers', 'JM': 'Rockets', 'Mayo': 'Spartans', 'Kellogg': 'Comets', 'Lincoln': 'Lynx'}

host = socket.gethostname()  # for outputting html
if host == "saturn":
    print('<!DOCTYPE html><html><head><title>RCC Winter Programming Competition 2021</title>')
    print('<link rel="stylesheet" href="stylesheets/styles.css">')
    print('<meta http-equiv="refresh" content="60" ><meta charset="UTF-8">')
    print('</head><body class="container">')
    print('<h1 class="rainbow">RAYTF & RCC Winter Programming Competition 2021 Leader-board</h1>')
    print(f"Updated at: {time.asctime()}\n")
    print("<h2 id='clock'>clock</h2>")

# print(time.time() - os.path.getmtime("data_file.json"))
# print(time.time(), os.path.getmtime("data_file.json"))
usefile = False  # get fresh data by default
# if it's been less than 15 minutes, just use what we had before.
filepath = "./"
if host == "saturn":
    filepath = "/var/www/html/python/AOCbot/"
if os.path.exists(filepath + "data_file.json") and time.time() - os.path.getmtime(filepath + "data_file.json") < 500:
    usefile = True  # if it's been less than 10 minutes, just use the stored file
# else:
#     print(f"Getting fresh data {time.time() - os.path.getmtime(filepath + 'data_file.json')}")

totalstars = 0
users = {}
schools = {}
teams = {}

if host == "saturn":
    with open(filepath + "users.json", "r") as read_file:
        users_json = json.load(read_file)
        for k in users_json.keys():
            users[k] = users_json[k]['What is your first and last name?']
            schools[k] = users_json[k]['Which school do you attend?']
            if users_json[k]['Are you participating as part of a team or as an individual?'] == 'Team':
                teams[k] = users_json[k]['What is your team name?']
else:
    userfile = 'users.csv'
    with open(userfile, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            # print(' *** '.join(row))
            users[row[5]] = row[2]
            schools[row[5]] = row[4]
            if row[7] == "Team":
                teams[row[5]] = row[8]
        csvfile.close()

    # add to a cleaned user dictionary for kenny
    jsondata = {}
    with open(userfile, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            # print(row)
            del row['Email Address']
            del row['What is your t-shirt size?']

            key = row['What is your Advent of Code Username? (Make sure you are logged in to see it!)']
            jsondata[key] = row

        csvfile.close()

    # Open a json writer, and use the json.dump()
    with open(filepath + 'users.json', 'w', encoding='utf-8') as jsonf:
        json.dump(jsondata, jsonf, indent=2)
        jsonf.close()

schoolstars = {}
numparticipants = {}
teamstars = {}

i_text = ""
t_text = ""
s_text = ""

if host == "saturn":
    i_text += ("\n<div id='individuals'>\n")
    i_text += ("\n<h2>Individuals:</h2><ol>\n")
else:
    i_text += ("\nIndividuals with at least one star:\n")

if usefile == True:
    with open(filepath + "data_file.json", "r") as read_file:
        data = json.load(read_file)
else:
    url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
    cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
    r = requests.get(url, cookies=cookies)
    # i_text += (r.text)
    data = json.loads(r.text)

    with open(filepath + "data_file.json", "w") as write_file:
        json.dump(data, write_file, indent=2)

starlist = []
for m in data["members"]:
    if data['members'][m]['stars']:
        #i_text += (m)
        #i_text += (data["members"][m])
        starlist.append(data["members"][m])

# resort the list by number of stars then local-score (reversed)
starlist = sorted(starlist, key=lambda starlist: (starlist['stars'], starlist['local_score']), reverse=True)
for entry in starlist:
    # if host != "saturn":
    #     print(users[entry['name']])
    if entry['name'] in teams:
        continue  # don't double-count team members!
    if entry['name'] in users:
        if host == "saturn":
            i_text += (f"<li><span class='{schools[entry['name']]}'>")
        i_text += (f"{users[entry['name']]} ({schools[entry['name']]}): {entry['stars']} stars")
        if host == "saturn":
            i_text += ("</span></li>")
        i_text += ("\n")

        if schools[entry['name']] in schoolstars:
            schoolstars[schools[entry['name']]] += entry['stars']
            numparticipants[schools[entry['name']]] += 1
        else:
            schoolstars[schools[entry['name']]] = entry['stars']
            numparticipants[schools[entry['name']]] = 1

        numparticipants['CTECH'] = 1

    else:
        if host == "saturn":
            # pass
            i_text += ("<li>")
            i_text += (f"{entry['name']} not registered - not counted: {entry['stars']} stars - go here to fix: <a href='https://forms.gle/kjF6wU71oXkJUaMD9'>https://forms.gle/kjF6wU71oXkJUaMD9</a>")
            i_text += ("</li>")
        else:
            i_text += (f"{entry['name']} not registered - not counted: {entry['stars']} stars")
        i_text += ("\n")


if host == "saturn":
    i_text += ("\n</ol>\n")
    i_text += ("If your name is on the AOC board, but not here, you probably didn't fill out the Google Form, or typed in your AOC username incorrectly.<br>\n")
    i_text += ("You can go here to fix it: <a href='https://forms.gle/kjF6wU71oXkJUaMD9'>https://forms.gle/kjF6wU71oXkJUaMD9</a>")
    i_text += ("</li>")
    i_text += ("</div>\n")
    t_text += ("\n<div id='teams'>\n")
    t_text += ("<h2>Teams:</h2>\n<ol>\n")
else:
    t_text += ("\nTeams:\n")

if usefile == True:
    with open(filepath + "team_file.json", "r") as read_file:
        data = json.load(read_file)
else:
    url = 'https://adventofcode.com/2021/leaderboard/private/view/1566841.json'
    cookies = dict(session='53616c7465645f5fc012ab039fb15a6fa623b7dca5a054d92e41ad9e667462260622bee83ecb5892e12d22b4b7aa579b')
    r = requests.get(url, cookies=cookies)
    # t_text += (r.text)
    data = json.loads(r.text)

    # I should really delete people who haven't registered here :/ JAB ***

    with open(filepath + "team_file.json", "w") as write_file:
        json.dump(data, write_file, indent=2)

# create the list of users and their stars
starlist = []
for m in data["members"]:
    if data['members'][m]['stars']:
        #t_text += (m)
        #t_text += (data["members"][m])
        starlist.append(data["members"][m])


# resort the list by number of stars (reversed)
starlist = sorted(starlist, key=lambda starlist: starlist['local_score'], reverse=True)
for entry in starlist:
    if entry['name'] in users:
        if entry['name'] not in teams:  # individual joined the team leaderboard
            continue
        if teams[entry['name']] in teamstars:
            # t_text += (f"skipping {users[entry['name']]}, already got {teams[entry['name']]} stars from other member")
            continue  # skip teams that already have a higher entry
        else:
            # t_text += (f"{teams[entry['name']]} : {entry['stars']} stars")
            teamstars[teams[entry['name']]] = entry['stars']

            if teams[entry['name']] == "Ctrl Alt Defeat":
                schoolstars["Mayo"] += entry['stars']
                numparticipants["Mayo"] += 1
                t_text += (f"<li class='Mayo'>Ctrl Alt Defeat (Mayo/Mayo): {entry['stars']} stars</li>")
            elif teams[entry['name']] == "CODINGBEASTS":
                schoolstars["Mayo"] += entry['stars']
                numparticipants["Mayo"] += 1
                t_text += (f"<li class='Mayo'>CODINGBEASTS (Mayo/Mayo): {entry['stars']} stars</li>")
            elif teams[entry['name']] == "Null Programmers Exception":
                schoolstars["Mayo"] += (entry['stars'] * 1) / 2.0
                schoolstars["Century"] += (entry['stars'] * 1) / 2.0
                numparticipants["Mayo"] += 0.5
                numparticipants["Century"] += 0.5
                t_text += (
                    f"<li style='color:#00CCCC'>Null Programmers Exception (Century/Mayo): {entry['stars']} stars</li>")
            elif teams[entry['name']] == "the kool kidz":
                schoolstars["Lincoln"] += entry['stars']
                numparticipants["Lincoln"] += 1
            elif teams[entry['name']] == "Strawberry":
                schoolstars["Lincoln"] += entry['stars']
                numparticipants["Lincoln"] += 1

    else:
        t_text += (f"ERROR!!! {entry['name']} : {entry['stars']} stars")

    t_text += ("\n")


if host == "saturn":
    t_text += ("\n</ol>\n</div>\n")
    s_text += ("\n<div id='schools'>\n")
    s_text += ("\n<h2>Schools:</h2>\n<ol>\n")
else:
    s_text += ("\nSchools:\n")


schoolstars = {k: v for k, v in sorted(schoolstars.items(), key=lambda item: item[1], reverse=True)}

animals = []
with open(filepath + "animals.txt", "r") as f:
    for line in f:
        animals.append(line.strip())
    f.close()

er = choice(["efficiency rating"])
for k in schoolstars:
    if host == "saturn":
        s_text += (f"<li><span class='{k}'>")

    totalstars += schoolstars[k]

    if k == "CTECH":
        s_text += (f"{k} : {schoolstars[k]:.1f} total stars, 1 {choice(animals)}, {schoolstars[k] / numparticipants[k]:.1f} {er}")
    else:
        s_text += (f"{k} : {schoolstars[k]:.1f} total stars, {numparticipants[k]:.1f} {mascots[k]}, {schoolstars[k] / numparticipants[k]:.1f} {er}")
    if host == "saturn":
        s_text += ("</span></li>")

if host == "saturn":
    s_text += ("</ol>")
    s_text += ("\n</div>\n")

print(s_text)
print(t_text)
print(i_text)

if host == "saturn":
    print("\n<div id='totalstars'>\n")
    print(f"\n<h2 class='rainbow'>Total Stars Earned by All Participants: {int(totalstars)}</h2>\n")
    print("\n</div>\n")
    print("<script src='scripts/main.js'></script>")
    print("\n</html></body>")
