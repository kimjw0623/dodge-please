import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('./chromedriver', options=options)
#regex = re.compile('[^a-zA-Z]')

summoners_id_list = []
#page_num=1
for page_num in range(21,41):
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

with open('id_list_2000_4000.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    spamwriter = csv.writer(csvfile)
    for i in range(len(summoners_id_list)):
        spamwriter.writerow([i,summoners_id_list[i]])

driver.quit()