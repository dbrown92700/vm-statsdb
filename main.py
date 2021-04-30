#!python3

from SDWAN import getStatsDb
#from gmail import send_gmail, send_email
import json, csv
from includes import baseurl, user, password
from datetime import datetime

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
#  Set up file
#
try:
    file = open('statsdb.csv','r')
    close(file)
except:
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
day_start = last_hour = []
for x in range(49):
    day_start += ['0']
    last_hour += ['0']
with open('statsdb.csv', 'r') as file:
    my_list = list(csv.reader(file))
for line in my_list:
    if (line[0] == str(month)) & (line[1] == str(day)) & (line[2] == '0'):
        day_start = line
last_hour = line

print(f'Midnight: {day_start}\nLast Hour: {last_hour}')

current = [month,day,hour]
num = 0
for stat in jstats['indexSize']:
    currentSize = float(stat['currentSize'].replace('gb',''))
    hour_delta = currentSize - float(last_hour[num*3 + 3])
    day_delta = currentSize - float(day_start[num*3 + 3])
    current += [stat['currentSize'].replace('gb',''), hour_delta, day_delta]
    num += 1
#    print(f"{stat['currentSize'].replace('gb','')},", end='')
print(current)
with open('statsdb.csv', 'a') as file:
    for field in current[:-1]:
        file.write(f'{field},')
    file.write(f'{field}\n')


'''
#
# Read previous global issues list from local file and save to set
#
oldissueset = set({})
infile = open('issueset.txt', 'r')
for lines in infile:
    oldissueset.add(lines.strip('\n'))
infile.close()

#
# Create new issues set and overwrite local file
# Add net new issues to an e-mail message
#
currentissueset = set({})
issue_count = 0
mail_body = ' new global issue(s) detected on DNA Center\n\n'
outfile = open('issueset.txt', 'w')
for issue in jissues['response']:
    currentissueset.add(issue[key])
    if issue[key] not in oldissueset:
        issue_count += 1
        mail_body += json.dumps(issue, indent=4).replace('"', '') + '\n'
    outfile.write(f"{issue[key]}\n")
outfile.close()
mail_body = str(issue_count) + mail_body

#
# calculate net new issues and send e-mail if new issues exist
#
newissues = currentissueset - oldissueset

if newissues == set({}):
    print('No new issues')
else:
    print('New Issues: ', newissues)
    if 'gmail.com' in from_user:
        send_gmail(gmail_user, gmail_password, recipient, 'THD DNAC Alert', mail_body)
    else:
        send_email(from_user, from_password, recipient, 'THD DNAC Alert', mail_body, mail_server, mail_port)
'''