#! /usr/bin/env python3

import sys
import operator
import re
import csv

errors = {}
per_user = {}

pattern = r'ticky: ([A-Z]+) (\w.*) \((\w.*)\)$'
with open(sys.argv[1], 'r') as file:
    for log in file.readlines():
        match = re.search(pattern, log)
        info, msg, usr = match.group(1), match.group(2), match.group(3)

        # add users to dictionary if not added yet
        if usr not in per_user.keys():
            per_user[usr] = {}
            per_user[usr]['INFO'] = 0
            per_user[usr]['ERROR'] = 0
        # update usr dictionary 
        if info == 'INFO':
            per_user[usr]['INFO']+=1
        elif info == 'ERROR':
            per_user[usr]['ERROR']+=1
        # update error dictionary if erro log found 
        if info == 'ERROR':
            if msg not in errors.keys():
                errors[msg] = 1
            else:
                errors[msg]+=1
# errors = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
errors_sorted = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
per_user_sorted = sorted(per_user.items(), key=operator.itemgetter(0))

with open('error.csv', 'w') as error:
    fieldnames = ['Error', 'Count']
    csvw = csv.DictWriter(error, fieldnames=fieldnames)
    csvw.writeheader()
    for key, value in errors_sorted:
        csvw.writerow({'Error': key, 'Count': value})
with open('user.csv', 'w') as error:
    fieldnames = ['Username', 'INFO', 'ERROR']
    csvw = csv.DictWriter(error, fieldnames=fieldnames)
    csvw.writeheader()
    for key, value in per_user_sorted:
        csvw.writerow({'Username': key, 'INFO': value['INFO'], 'ERROR': value['ERROR']})
