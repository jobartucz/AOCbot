import requests
import json

url = 'https://adventofcode.com/2021/leaderboard/private/view/641987.json'
cookies = dict(session='53616c7465645f5f72b4a0ed3b4c9147b26da9702562b6c77828a4bdefb2d9c8bed1773bf0f4e7899e48c8be77e15431')
r = requests.get(url, cookies=cookies)
print(r.text)
json.dumps(r.text, indent=4, separators=(". ", " = "))