from cgitb import small
import time
import csv
import re
import ast

# match example:
# "[['Riven', 'Azhy', 'RekSai', 'kratosase', 'Zoe', 'qwesadz', 'Kaisa', '잘생긴오현택', 'Nautilus', '후회없는인생살게', 'Qiyana', 'EQWEQWRGFREGRE', 'Hecarim', 'lilliillilllilii', 'Swain', 'QXAL972184346', 'Samira', 'yiqunlanzi', 'Sett', 'liang mian']
#   [True, '17분 48초']]"

unknown_ids = {}

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

def get_statistics(match_list):
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

def gen_id_info_dict():
    id_to_info = {}
    id_list = []
    info_list = []
    with open('id_list.csv', mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            id_list.append(rows[1])

    with open('id_list_1000_2000.csv', mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            id_list.append(rows[1])

    with open('id_list_2000_4000.csv', mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            id_list.append(rows[1])

    with open('id_info_list_1000.csv', mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            info_list.append(ast.literal_eval(rows[1]))

    with open('id_info_list_1000_2000.csv', mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            info_list.append(ast.literal_eval(rows[1]))

    with open('id_info_list_2000_4000.csv', mode='r', encoding='utf-8-sig') as inp:
        reader = csv.reader(inp)
        for rows in reader:
            small_list = []
            for i in rows:
                small_list.append(ast.literal_eval(i))
            info_list.append(small_list)

    for id, info in zip(id_list, info_list):
        id_to_info[id] = info

    return id_to_info

def get_id_champ_info(info_dict, champion, player_id):
    winrate = -1
    total_match = -1
    try:
        for elem in info_dict[player_id]:
            champ = regex.sub('', elem[0]).lower()
            if champ == champion:
                winrate = elem[1]
                total_match = elem[2] + elem[3]
                break
    except:
        winrate = -2
        total_match = -2
        if not player_id in unknown_ids:
            unknown_ids[player_id] = 1
        else:
            unknown_ids[player_id] += 1
        #unknown_ids.append(player_id)
    
    return winrate, total_match

# Return champ embedding vector
def champ_embedding():
    dict_from_csv = {}
    regex = re.compile('[^a-zA-Z]')

    with open('champ_list.csv', mode='r') as inp:
        reader = csv.reader(inp)
        dict_from_csv = {regex.sub('', rows[1]).lower():rows[0] for rows in reader}

    return dict_from_csv

champ_vector_dict = champ_embedding()

regex = re.compile('[^a-zA-Z]')

matches_1000 = get_unique_matches('match_info_list_1000.csv')
# matches_1000_2000 = get_unique_matches('match_info_list_1000_2000.csv')

match_list = list(set(matches_1000))# + matches_1000_2000))

#get_statistics(match_list)

id_info_dict = gen_id_info_dict()

match_dataset = []

for match in match_list:
    match_vector = []
    champ = 'default'
    for i in range(10):
        champ = regex.sub('', match[0][2*i]).lower()
        winrate, match_count = get_id_champ_info(id_info_dict, champ, match[0][2*i + 1])
        champ = int(champ_vector_dict[champ])
        match_vector.append(champ) 
        match_vector.append(int(winrate))
        match_vector.append(int(match_count))

    match_dataset.append(match_vector)

print(match_dataset[:10])

#unknown_ids = list(set(unknown_ids))

#print(len(unknown_ids))