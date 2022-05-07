import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('./chromedriver', options=options)
regex = re.compile('[^a-zA-Z]')

def get_winrate(champ_name, summoners_id):
    winrate_url = f'https://www.op.gg/summoners/kr/{summoners_id}/champions'
    driver.get(winrate_url) 
    time.sleep(1)
    #driver.find_element_by_xpath('//*[@id="content-container"]/div/div/div[2]/button[2]').click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find('table').find('tbody').find_all('tr')#, class_='rank css-1wvfkid exo2f211')
    #print(info)
    winrate = 0
    num_win_match = 0
    num_lose_match = 0
    for champ_info in info:
        #champ_info = champ_info.find('td')
        # print(champ_info)
        try: # Some summoners changed id
            champ = champ_info.find('td', class_='summoner-name').find('a').get('href').split('/')[2]
            champ = regex.sub('', champ).lower()
            champ_name = regex.sub('', champ_name).lower()
            if champ != champ_name:
                continue
            winrate = int(champ_info.find('div', class_='win-ratio').find('span').text[:-1])
            try:
                num_win_match = int(champ_info.find('td', class_='summoner-name').find_next_sibling('td').find('div',class_='winratio-graph__text left').text[:-1])
            except:
                num_win_match = 0
            try:
                num_lose_match = int(champ_info.find('td', class_='summoner-name').find_next_sibling('td').find('div',class_='winratio-graph__text right').text[:-1])
            except:
                num_lose_match = 0
            #print(champ, winrate, num_win_match+num_lose_match)
            break
        except:
            winrate = -1
            num_win_match = -1
            num_lose_match = 0
        
    return champ_name, winrate, num_win_match+num_lose_match

def get_matches(ids):
    '''
        ref docstring!

        output: match: (blue_top_summoner_id, blue_top_champ_name, ...)
    '''
    for summoners_id in ids:
        info_url = f'https://www.op.gg/summoners/kr/{summoners_id}'
        driver.get(info_url) 
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # match_info
        train_dataset = []
        train_dataset_result = []

        idx = 0

        for tag in soup.find_all('li',class_='css-ja2wlz e19epo2o3'):#'css-1qq23jn e1iiyghw3'):
            if idx == 5:
                break
            idx += 1
            if tag.find('div', class_='type').text != '솔랭':
                continue
            # match_length = tag.find('div', class_ = 'game-length').text
            isWin = tag.find('div').get('result')
            isWin = True if isWin=='WIN' else False

            participants = tag.find_all('li', class_='css-tegtkt e19epo2o1')#'css-15pg66g e1iiyghw1')

            red_participants, blue_participants = (participants[0].find_parent('ul').find_next_siblings('ul')[0].find_all('li'),
                                                participants[0].find_parent('ul').find_all('li'))

            # Change to function?
            blue_team_champ = []
            blue_team_id = []
            for i in blue_participants:
                blue_team_champ.append(i.find('div', class_='icon').find('img').get('src').split('/')[6].split('.')[0])
                blue_team_id.append(i.find('div', class_='name').find('a').text)
            
            red_team_champ = []
            red_team_id = []
            for i in red_participants:
                red_team_champ.append(i.find('div', class_='icon').find('img').get('src').split('/')[6].split('.')[0])
                red_team_id.append(i.find('div', class_='name').find('a').text)

            assert len(blue_team_champ),len(blue_team_id) == (5,5)
            assert len(red_team_champ),len(red_team_id) == (5,5)

            train_data = []

            # win = True: blue team win
            if isWin:
                win = True if summoners_id in blue_team_id else False
            else:
                win = False if summoners_id in blue_team_id else True

            for i in range(5):
                train_data.append(blue_team_champ[i])
                train_data.append(blue_team_id[i])
            for i in range(5):
                train_data.append(red_team_champ[i])
                train_data.append(red_team_id[i])
            
            train_dataset.append(train_data)
            print(train_data)
            train_dataset_result.append(win)
            print(win)

            # print(win)
            # print('blue')
            # print(blue_team_champ)
            # print(blue_team_id)
            # print('red')
            # print(red_team_champ)
            # print(red_team_id)
            
    return train_dataset, train_dataset_result

def get_ids():
    summoners_id_list = []
    page_num=1
    info_url = f'https://www.op.gg/leaderboards/tier?page={page_num}&region=kr'
    driver.get(info_url) 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get top5 summoners
    if page_num == 1:
        top5 = soup.select_one('div', class_='css-1j84o5i ei93w703')
        top1 = top5.find('a',class_='name')
        summoners_id_list.append(top1.text) 

        top5 = top5.find_all('span', class_ = 'name')
        for i in range(4):
            summoners_id_list.append(top5[i].text) 

    others = soup.select_one('table', class_= 'css-131ws48 ei93w701')
    rows = others.select('tr',class_='css-1xdhyk6 ei93w700')
    for i in range(len(rows)-1):
        summoners_id_list.append(rows[i+1].find('strong').text)

    return summoners_id_list

# Return champ embedding vector
def champ_embedding():
    dict_from_csv = {}
    regex = re.compile('[^a-zA-Z]')

    with open('champ_list.csv', mode='r') as inp:
        reader = csv.reader(inp)
        dict_from_csv = {regex.sub('', rows[1]).lower():rows[0] for rows in reader}

    return dict_from_csv


# (blue_team_info, red_team_info), (result)
# blue_team_info: (top_champ, top_champ_winrate, top_champ_match_count, jg ..., mid ..., sup ...)
# TODO:
# 1. decide whether use DB or pandas or numpy file to save data
# 2. add command line arguments: users can decide whether to use pre-generated data or to generate (crawling) new data
def generate_dataset():
    regex = re.compile('[^a-zA-Z]')
    champ_vector_dict = champ_embedding()
    gen_summoner_ids = True
    summoner_ids = []

    # Get summoner's ids
    if gen_summoner_ids:
        summoner_ids = get_ids()
    else:
        summoner_ids = get_ids()
        #read local dataset
    
    # Get raw match data
    matches, matches_result = get_matches([summoner_ids[0]])

    # 
    matches_data = []
    matches_result_data = []
    for match in matches:
        match_vector = []
        for i in range(10):
            champ, winrate, match_count = get_winrate(match[2*i],match[2*i+1])
            print(winrate)
            champ = regex.sub('', champ).lower()
            print(champ)
            champ = int(champ_vector_dict[champ])
            match_vector.append(champ) 
            match_vector.append(int(winrate))
            match_vector.append(int(match_count))
        matches_data.append(match_vector)
        #matches_result_data.append(match[-1])
    
    print(matches_data)
    print(matches_result)
    # save train_data and test_data

if __name__ == '__main__':
    # get_matches(['타 잔'])
    # print(get_winrate('타 잔','leesin'))
    # get_ids()
    
    generate_dataset()
    driver.quit()
