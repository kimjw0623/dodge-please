from cgitb import small
import time
import csv
import re
import ast

# 3000

train_list = []
test_list = []
idx = 0
with open('data/match_info_embedded_ver4.csv', mode='r', encoding='utf-8-sig') as inp:
    reader = csv.reader(inp)
    for rows in reader:
        idx += 1
        if idx < 35001:
            train_list.append((rows[0],rows[1]))
        else:
            test_list.append((rows[0],rows[1]))

with open('data/match_info_embedded_ver4_train.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for match in train_list:
        spamwriter.writerow((match[0],match[1]))
    
with open('data/match_info_embedded_ver5_test.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for match in test_list:
        spamwriter.writerow((match[0],match[1]))

        
# print(len(train_list), len(test_list))
# print(train_list[:2])
# print(test_list[:2])