import requests
from bs4 import BeautifulSoup
import re
# import pymongo

# conn = pymongo.MongoClient()
# db_opgg = conn.opgg
# db_opgg_rank = db_opgg.rank

opgg_link = 'https://www.op.gg/ranking/ladder/' #API 요청 링크
data = requests.get(opgg_link).content
soup = BeautifulSoup(data, 'html.parser')

# 1 ~ 5 ranking highest
ranking_highest = soup.select('li.ranking-highest__item')
print(ranking_highest)