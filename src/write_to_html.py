#!/usr/bin/python3

import datetime
from datetime import datetime, timedelta
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

def update_date(country):
    _country_ = country.lower().replace(" ", "_")
    country = country.lower().replace(" ", "")

    dir_path = os.path.dirname(os.path.realpath(__file__))[0:56] + "/src/htmls/" + country + ".html"
    print(dir_path)

    date_aot = str(datetime.today())[0:10]
    date_aoy = str(datetime.today() - timedelta(days=1))[0:10]
    date_ao2 = str(str(datetime.today() - timedelta(days=2))[0:10])
    date_ao3 = str(str(datetime.today() - timedelta(days=2))[0:10])

    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            if date_aoy in line:
                newstr += line.replace(date_aoy, date_aot)
            elif date_ao2 in line:
                newstr += line.replace(date_ao2, date_aot)
            elif date_ao3 in line:
                newstr += line.replace(date_ao3, date_aot)
            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

def update_index():
    req = Request('https://www.worldometers.info/coronavirus/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = BeautifulSoup(page, 'html.parser')
    world_numbers_html = page.findAll("div", class_="maincounter-number")

    world_numbers = []

    for number in world_numbers_html:
        finder = re.compile(r'(\d{0,3},)(\d{3},)?\d{0,3}')
        for match in finder.finditer(str(number)):
            world_numbers.append(match.group())

    # print(total_cases)

    dir_path = os.path.dirname(os.path.realpath(__file__))[0:56] + "/index.html"
    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            if "World Cases" in line:
                newstr += '					<h3>World Cases: <span style="color: blue;">' + world_numbers[0] + \
                          '</span> &emsp; &emsp; &emsp; World Deaths: <span style="color: red;">' + world_numbers[1] + \
                          '</span> &emsp; &emsp; &emsp; Recovered: <span style="color: rgb(15, 146, 15);">' + \
                          world_numbers[2] + '</span></h3>'
            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()
# update_index()

# if __name__ == "__main__":
#     country = str(sys.argv[1])
#     update_date(country)

mycountries = ['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
for country in mycountries:
    update_date(country)
