import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import re
from random import randint

regex = re.compile('[^a-zA-Z]')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('./chromedriver', options=options)

ids = []
results = []

with open('data/id_list_15000_5_31.csv', mode='r', encoding='utf-8-sig') as inp:
    reader = csv.reader(inp)
    for rows in reader:
        ids.append(rows[1])

#ids = ids[1200:1203]
with open('data/id_info_list_15000_5_31.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    info_url = f'https://www.op.gg/leaderboards/tier?page=1&region=kr'
    driver.get(info_url) 
    for summoners_id in ids:
        rand_value = randint(1, 5)
        time.sleep(rand_value)
        print(summoners_id)
        winrate_url = f'https://www.op.gg/summoners/kr/{summoners_id}/champions'
        tier_url = f'https://www.op.gg/summoners/kr/{summoners_id}'
        
        # Get tier info
        try:
            driver.get(tier_url) 
        except:
            spamwriter.writerow(['None','None','None','None'])
            continue
    
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            #print(soup.find('div', class_='css-19ozhet e1sjz9pt1').find('div', class_='css-13uv2u8 e135kpg1').find('div', class_='info'))#find('div', class_='wapper').
            tier_class = soup.find('div', class_='css-19ozhet e1sjz9pt1').find('div', class_='css-13uv2u8 e135kpg1').find('div',class_='info')
            #print(tier_class)
            tier_type = tier_class.find('div', class_='tier-rank').text
            print(tier_type)
            tier_point = tier_class.find('div', class_='tier-info').find('span', class_='lp').text[:-3]
            print(tier_type, tier_point)
        except:
            print('tier lost')
            spamwriter.writerow(['None','None','None','None'])
            continue
        
        # Get champ winrate info
        rand_value = randint(1, 5)
        time.sleep(rand_value)
        try:
            driver.get(winrate_url) 
        except:
            spamwriter.writerow(['None','None','None','None'])
            continue
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print('next')
        try:
            info = soup.find('table').find('tbody').find_all('tr')#, class_='rank css-1wvfkid exo2f211')
        except:
            spamwriter.writerow(['None','None','None','None'])
            #results.append(['None'])
            continue
        #print(info)
        winrate = 0
        num_win_match = 0
        num_lose_match = 0
        id_info = []

        for champ_info in info:
            #champ_info = champ_info.find('td')
            # print(champ_info)
            try: # Some summoners changed id
                champ = champ_info.find('td', class_='summoner-name').find('a').get('href').split('/')[2]
                champ = regex.sub('', champ).lower()
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
            except:
                champ = 'none'
                winrate = -1
                num_win_match = -1
                num_lose_match = -1

            id_info.append((champ, winrate, num_win_match, num_lose_match))
        
        spamwriter.writerow([summoners_id, tier_type, tier_point ,id_info])
        
driver.quit()