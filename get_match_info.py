import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import re

regex = re.compile('[^a-zA-Z]')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('./chromedriver', options=options)

ids = []
total_match_info = []
total_match_result = []

with open('data/id_list_15000.csv', mode='r', encoding='utf-8-sig') as inp:
    reader = csv.reader(inp)
    for rows in reader:
        ids.append(rows[1])

ids = ids[:2000]

with open('match_info_list_ver5.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for summoners_id in ids:
        print(summoners_id)
        info_url = f'https://www.op.gg/summoners/kr/{summoners_id}'
        try:
            driver.get(info_url) 
            # driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/button').click()
            # driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/button').click()
            # driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/button').click()
            # driver.find_element_by_xpath('//*[@id="__next"]/div[5]/div[2]/button').click()
            time.sleep(4)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # match_info
            train_dataset = []
            train_dataset_result = []
        except:
            continue

        idx = 0
        try:
            matches = soup.find_all('li',class_='css-ja2wlz e19epo2o3')
        except:
            continue
        
        for tag in matches:#'css-1qq23jn e1iiyghw3'):
            game_type = tag.find('div', class_='type')
            if game_type.text != '솔랭':
                continue
            time_info = game_type.find_next_sibling('div').find('div', class_='time-stamp').text
            print(time_info)
            if '일' in time_info:
                continue

            match_length = tag.find('div', class_ = 'game-length').text
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
            train_dataset_result.append([win,match_length])

            assert len(train_dataset) == len(train_dataset_result)

        
        spamwriter.writerow([train_dataset,train_dataset_result])

        #total_match_info.append(train_dataset)
        #total_match_result.append(train_dataset_result)


driver.quit()