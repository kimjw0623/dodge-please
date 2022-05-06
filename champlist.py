import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('./chromedriver', options=options)

# Get list of champions
champ_list = []

winrate_url = f'https://lol.fandom.com/wiki/Portal:Champions/List'
driver.get(winrate_url) 
time.sleep(1) 
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.close()
champs_info = soup.find('table', class_='sortable wikitable smwtable jquery-tablesorter').find('tbody').find_all('tr')

for i in range(len(champs_info)):
    champ_name = champs_info[i].find('td').find('span',class_='champion-object')
    champ_name = champ_name.find('a').get('href').split('/')[-1]
    champ_list.append(champ_name)

# Save to .scv
with open('champ_list.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for i in range(len(champ_list)):
        spamwriter.writerow([i,champ_list[i]])
