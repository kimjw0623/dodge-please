import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

  
# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('./chromedriver') 



# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
# summoners_id_list = []
# for page_num in range(1,2):
#     url = f'https://www.op.gg/leaderboards/tier?page={page_num}&region=kr'
#     resp = requests.get(url,headers = headers)
#     soup = BeautifulSoup(resp.text, 'html.parser')

#     # Get top5 summoners
#     if page_num == 1:
#         top5 = soup.select_one('div', class_='css-1j84o5i ei93w703')
#         top1 = top5.find('a',class_='name')
#         summoners_id_list.append(top1.text) 

#         top5 = top5.find_all('span', class_ = 'name')
#         for i in range(4):
#             summoners_id_list.append(top5[i].text) 

#     others = soup.select_one('table', class_= 'css-131ws48 ei93w701')
#     rows = others.select('tr',class_='css-1xdhyk6 ei93w700')
#     for i in range(len(rows)-1):
#         summoners_id_list.append(rows[i+1].find('strong').text)

# print(summoners_id_list)

summoners_id = ''
summoners_id_list = ['타 잔']
winrate_url = f'https://www.op.gg/summoners/kr/{summoners_id}/champions'

for summoners_id in summoners_id_list:
    print(summoners_id)
    info_url = f'https://www.op.gg/summoners/kr/{summoners_id}'
    driver.get(info_url) 
    time.sleep(2) 
    html = driver.page_source
    #info_resp = requests.get(info_url,headers = headers)
    soup = BeautifulSoup(html, 'html.parser')
    
    #print(soup.find_all('div',class_='game_result'))
    #print(soup.find_all('li',class_='css-1sq1kbv e3mqlfu0'))
    # match_info
    for tag in soup.find_all('li',class_='css-ja2wlz e19epo2o3'):
        if tag.find('div', class_='type').text != 'Ranked Solo':
            continue
        print(tag.find('div', class_ = 'game-result').text)
        print(tag.find('div', class_ = 'game-length').text) 
        print(tag.find('div', class_ = 'type').text)
        isWin = tag.find('div').get('result') #'css-4nxc2y e19epo2o2'
        isWin = True if isWin=='WIN' else False

        participants = tag.find_all('li', class_='css-tegtkt e19epo2o1')

        blue_participants, red_participants = (participants[0].find_parent('ul').find_next_siblings('ul')[0].find_all('li'),
                                              participants[0].find_parent('ul').find_all('li'))

        # Change to function?
        blue_team_champ = []
        blue_team_id = []
        for i in blue_participants:
            blue_team_champ.append(i.find('div', class_='icon').find('img').get('alt'))
            blue_team_id.append(i.find('div', class_='name').find('a').text)
        
        red_team_champ = []
        red_team_id = []
        for i in red_participants:
            red_team_champ.append(i.find('div', class_='icon').find('img').get('alt'))
            red_team_id.append(i.find('div', class_='name').find('a').text)

        assert len(blue_team_champ),len(blue_team_id) == (5,5)
        assert len(red_team_champ),len(red_team_id) == (5,5)

        if isWin:
            win = 'blue' if summoners_id in blue_team_champ else 'red'
        else:
            win = 'red' if summoners_id in blue_team_champ else 'blue'
        
        print(win)
        print(blue_team_champ)
        print(blue_team_id)
        print(red_team_champ)
        print(red_team_id)


        #print(participants[0])
        #for champ_idx in range(9):
        #    print(participants[champ_idx].find('div', class_='icon').find('img').get('alt'))
    break

        # champs = tag.find_all('css-tegtkt e19epo2o1')
        # champs = champs.find('div.participants')
        # champs = champs.select('ul > li > div.icon')
        # for idx in range(10):
        #     print(champs.get('alt'))
        
    
    # summoner's status



    # full_info = soup.select_one('div', class_='css-19ozhet e1sjz9pt1')
    # #print(full_info)
    # game_info = full_info.select_one('div', class_='css-1sq1kbv e3mqlfu0')
    
    # game_info = game_info.select('ul', class_='css-164r41r exlvoq30')
    # #print(game_info)
    # game_list = game_info.find_all('div', class_='css-utzuox e19epo2o2')
    # #print(game_list[0])