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
results = []

with open('id_list_2000_4000.csv', mode='r', encoding='utf-8-sig') as inp:
    reader = csv.reader(inp)
    for rows in reader:
        ids.append(rows[1])

#ids = ids[:100]
with open('id_info_list_2000_4000.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for summoners_id in ids:
        print(summoners_id)
        winrate_url = f'https://www.op.gg/summoners/kr/{summoners_id}/champions'
        driver.get(winrate_url) 
        time.sleep(4)
        #driver.find_element_by_xpath('//*[@id="content-container"]/div/div/div[2]/button[2]').click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            info = soup.find('table').find('tbody').find_all('tr')#, class_='rank css-1wvfkid exo2f211')
        except:
            results.append([0])
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
        
        spamwriter.writerow(id_info)
        #results.append(id_info)
    
# with open('id_info_list_1000_2000.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for i in range(len(results)):
#         spamwriter.writerow([i,results[i]])

driver.quit()