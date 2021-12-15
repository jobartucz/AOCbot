import json
from datetime import datetime

with open("data_file.json", "r") as read_file:
    data = json.load(read_file)

times = {}

times['2'] = int((datetime(2021, 12, 2) - datetime(1970, 1, 1)).total_seconds()) + 21600 - 3600
times['9'] = int((datetime(2021, 12, 9) - datetime(1970, 1, 1)).total_seconds()) + 21600 - 3600
times['16'] = int((datetime(2021, 12, 16) - datetime(1970, 1, 1)).total_seconds())
times['23'] = int((datetime(2021, 12, 23) - datetime(1970, 1, 1)).total_seconds())
times['30'] = int((datetime(2021, 12, 30) - datetime(1970, 1, 1)).total_seconds())

print(times)

mins = {}
mins['2'] = ('',99999999999,'')
mins['9'] = ('',99999999999, '')
mins['16'] = ('',99999999999, '')
mins['23'] = ('',99999999999, '')
mins['30'] = ('',99999999999, '')

for k in data['members'].keys():
    if '1' in data['members'][k]['completion_day_level']:
        for t in mins.keys():
            diff = data['members'][k]['completion_day_level']['1']['1']['get_star_ts'] - times[t]
            if diff > 0 and diff < mins[t][1]:
                mins[t] = (data['members'][k]['name'],diff,datetime.fromtimestamp(data['members'][k]['completion_day_level']['1']['1']['get_star_ts']).strftime('%Y-%m-%d %H:%M:%S'))
                print(data['members'][k]['completion_day_level']['1']['1']['get_star_ts'], t,   data['members'][k]['name'],diff,datetime.fromtimestamp(data['members'][k]['completion_day_level']['1']['1']['get_star_ts']).strftime('%Y-%m-%d %H:%M:%S'))

for t in mins.keys():
    if mins[t][1] != 99999999999:
        print(f"Thursday, December {t}: {mins[t]}")

