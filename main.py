#!python3

import json, csv, os.path
from datetime import datetime, timedelta

from SDWAN import getStatsDb
from includes import baseurl, user, password, from_user, from_password, mail_server, mail_port, recipient, alert_title
from gmail import send_email, send_gmail, create_email

#
# Grab Time
#

now = datetime.now()
month = now.month
day = now.day
hour = now.hour

#
#  Pull API data
#

stats = getStatsDb(baseurl, user, password)
jstats = json.loads(stats)

#
#  Set up file if it doesn't exist
#

if not os.path.exists('statsdb.csv'):
    file = open('statsdb.csv', 'w')
    file.write('Month,Day,Hour,')
    for stat in jstats['indexSize'][:-1]:
        file.write(f"{stat['displayName']},{stat['displayName']} Hour,{stat['displayName']} Day,")
    stat = jstats['indexSize'][-1]
    file.write(f"{stat['displayName']},{stat['displayName']} Hour,{stat['displayName']} Day\n{month},{day},0,")
    for x in range(len(jstats['indexSize'])-1):
        file.write('0,0,0,')
    file.write('0,0,0\n')
    file.close()

#
# Grab previous Stats
#

with open('statsdb.csv', 'r') as file:
    my_list = list(csv.reader(file))
for line in my_list:
    if hour != 0:
        if (line[0] == str(month)) & (line[1] == str(day)) & (line[2] == '0'):
            day_start = line
    else:
        day_before = (now - timedelta(days = 1)).day
        month_before = (now - timedelta(days = 1)).month
        if (line[0] == str(month_before)) & (line[1] == str(day_before)) & (line[2] == '0'):
            day_start = line
last_hour = line

#
# Generate current stats and write to file
#

current = [month,day,hour]
num = 0
for stat in jstats['indexSize']:
    currentSize = float(stat['currentSize'].replace('gb',''))
    hour_delta = currentSize - float(last_hour[num*3 + 3])
    day_delta = currentSize - float(day_start[num*3 + 3])
    current += [stat['currentSize'].replace('gb',''), hour_delta, day_delta]
    num += 1
with open('statsdb.csv', 'a') as file:
    for field in current[:-1]:
        file.write(f'{field},')
    file.write(f'{current[-1]}\n')

#
# Send email at the end of the day
#

if hour == 12:
    message = create_email(from_user, recipient, alert_title, 'Home Depot daily StatsDB file', 'statsdb.csv')
    if 'gmail.com' in from_user:
        send_gmail(from_user, from_password, recipient, message)
    else:
        send_email(from_user, recipient, message, mail_server, mail_port)
