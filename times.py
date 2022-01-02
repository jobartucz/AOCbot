### individual:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
# cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
### team:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/1566841.json'
# cookies = dict(session='53616c7465645f5fc012ab039fb15a6fa623b7dca5a054d92e41ad9e667462260622bee83ecb5892e12d22b4b7aa579b')
### college:
# url = 'https://adventofcode.com/2021/leaderboard/private/view/1567131.json'
# cookies = dict(session='53616c7465645f5f6af580b520db3b7acaa0d4a0f305ef5188fa1e2e4f8e0b2ff13c15bd22f17fb790eb64602b09311c')


import json
import time
import socket
from datetime import datetime

host = socket.gethostname() # for outputting html

# print(time.time() - os.path.getmtime("data_file.json"))
# print(time.time(), os.path.getmtime("data_file.json"))
usefile = False # get fresh data by default
# if it's been less than 15 minutes, just use what we had before.
filepath = "./"
if host == "saturn":
    filepath = "/var/www/html/python/AOCbot/"

times = {}

for i in range(1,26):
    times[i] = int((datetime(2021, 12, i) - datetime(1970, 1, 1)).total_seconds()) + 18000
    # print(times[i])
    # print(f"{datetime.fromtimestamp(times[i]).strftime('%Y-%m-%d %H:%M:%S')}")

users = {}

with open(filepath + "users.json", "r") as read_file:
        users_json = json.load(read_file)
        for k in users_json.keys():
            users[k] = users_json[k]['What is your first and last name?']


with open(filepath + "data_file.json", "r") as read_file:
    data = json.load(read_file)

starlist = []
for m in data["members"]:
    if data['members'][m]['stars']:
        starlist.append(data["members"][m])


with open(filepath + "team_file.json", "r") as read_file:
    team_data = json.load(read_file)

for m in team_data["members"]:
    if team_data['members'][m]['stars']:
        duplicate = False
        for n in data["members"]:
            if m == n:
                duplicate = True
        if duplicate == False:
            starlist.append(team_data["members"][m])

with open("times.csv", "w") as f:
    f.write("Day,")
    for i in range(1,26):
        f.write(f"D {i} P 1,D {i} P 2,")
    f.write("\n")


    # resort the list by number of stars then local-score (reversed)
    starlist = sorted(starlist, key = lambda starlist: (starlist['stars'], starlist['local_score']),reverse=True)
    for entry in starlist:
        # if host != "saturn":
        #     print(users[entry['name']])
        if entry['name'] in users:
            print(f"\n{users[entry['name']]}: {entry['stars']} stars")

            f.write(f"{users[entry['name']]},")
            for i in range(1,26):
                if str(i) in entry['completion_day_level']:

                    print(f"Day {i}:")
                    if str('1') in entry['completion_day_level'][str(i)]:
                        diff = entry['completion_day_level'][str(i)]['1']['get_star_ts'] - times[i]
                        days, remainder = divmod(diff, 3600*24)
                        hours, remainder = divmod(remainder, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        print("  Part 1: {:02}:{:02}:{:02}:{:02}".format(int(days), int(hours), int(minutes), int(seconds)))
                        f.write(str(diff))
                    f.write(',')

                    if str('2') in entry['completion_day_level'][str(i)]:
                        diff = entry['completion_day_level'][str(i)]['2']['get_star_ts'] - entry['completion_day_level'][str(i)]['1']['get_star_ts']
                        days, remainder = divmod(diff, 3600*24)
                        hours, remainder = divmod(remainder, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        print("  Part 2: {:02}:{:02}:{:02}:{:02}".format(int(days), int(hours), int(minutes), int(seconds)))
                        f.write(str(diff))
                    f.write(',')
            f.write('\n')


        else:

            print(f"{entry['name']} not registered - not counted: {entry['stars']} stars")


