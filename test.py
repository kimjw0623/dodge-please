import requests
from bs4 import BeautifulSoup
import re
import csv
import ast

with open('more_match_info_list_1000.csv', mode='r', encoding='utf-8-sig') as inp:
    reader = csv.reader(inp)
    for rows in reader:
        print(len(ast.literal_eval(rows[1])))
        break