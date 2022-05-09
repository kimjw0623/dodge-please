import time
import csv
import re
import ast
#"[['Riven', 'Azhy', 'RekSai', 'kratosase', 'Zoe', 'qwesadz', 'Kaisa', '잘생긴오현택', 'Nautilus', '후회없는인생살게', 'Qiyana', 'EQWEQWRGFREGRE', 'Hecarim', 'lilliillilllilii', 'Swain', 'QXAL972184346', 'Samira', 'yiqunlanzi', 'Sett', 'liang mian']
#  [True, '17분 48초']]"

def get_unique_matches(file_name):
    match_list = []
    with open(file_name, mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            matches = ast.literal_eval(rows[0])
            results = ast.literal_eval(rows[1])
            assert len(matches) == len(results)

            for i in range(len(matches)):
                match_list.append((tuple(matches[i]),tuple(results[i])))

    return list(set(match_list))

matches_1000 = get_unique_matches('match_info_list_1000.csv')
matches_1000_2000 = get_unique_matches('match_info_list_1000_2000.csv')

match_list = list(set(matches_1000 + matches_1000_2000))

final_num_matches = len(match_list)

champ_dict = {}
id_list = []
num_blue_win = 0
num_red_win = 0

for match in match_list:
    for i in range(10):
        id_list.append(match[0][2*i+1])

        champ_name = match[0][2*i]
        if not champ_name in champ_dict:
            champ_dict[champ_name] = 1
        else:
            champ_dict[champ_name] += 1

    if match[1][0]:
        num_blue_win += 1
    else: 
        num_red_win += 1

id_list = list(set(id_list))

print(champ_dict)
print(f'# of total_matches: {final_num_matches}')
print(f'# of ids: {len(id_list)}')
print(f'Blue team win: {num_blue_win}, red team win: {num_red_win}, total: {final_num_matches}')
