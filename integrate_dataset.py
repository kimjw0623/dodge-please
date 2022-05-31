from cgitb import small
import time
import csv
import re
import ast

# TODO:
# 1. delete row that contains -2 more than 2
# 2. integrate and shuffle
# 3. generate train/testset

def delete_matches(file_name):
    match_list = []
    with open(file_name, mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            match_input = ast.literal_eval(rows[0])
            if match_input.count('-2') > 4:
                continue
            match_list.append((rows[0],rows[1]))
            
    return match_list

total_match_list = []

# delete row that contains -2 more than 2
match1 = delete_matches('data/match_info_embedded_ver_5_23_test (1).csv')
total_match_list.extend(match1)
match2 = delete_matches('data/match_info_embedded_ver_5_23_test.csv')
total_match_list.extend(match2)
match3 = delete_matches('data/match_info_embedded_5_26_5_30_test.csv')
total_match_list.extend(match3)
       
print(total_match_list[0])
# integrate and shuffle
total_match_list = list(set(total_match_list))
print(len(total_match_list))

# generate train/testset
idx = 0
with open('dataset/match_info_embedded_5_31_train.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for match in total_match_list[:9000]:
        spamwriter.writerow((match[0],match[1]))
    
with open('dataset/match_info_embedded_5_31_test.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for match in total_match_list[9001:]:
        spamwriter.writerow((match[0],match[1]))