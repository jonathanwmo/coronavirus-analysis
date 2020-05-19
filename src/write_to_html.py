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

def get_country_data(country):
    country = country.lower().replace(" ", "-")
    if country == "united-states":
        country = "us"
    elif country == "united-kingdom":
        country = "uk"

    req = Request('https://www.worldometers.info/coronavirus/', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = BeautifulSoup(page, 'html.parser')

    page_list = str(page).split("\n")

    country_numbers_html = []
    inlines = False

    for line in page_list:
        if ("country/" + country + "/") in str(line.strip()):
            inlines = True
        if inlines == True:
          country_numbers_html.append(line)
        if ('a href="/world-population/' + country + "-population/") in str(line):
            break

    country_numbers_html = country_numbers_html[1:]
    country_numbers = []
    for i in range(len(country_numbers_html)):
        myList = [country_numbers_html[i]]
        for line in myList:
            finder = re.compile(r'(\d{0,3},)?((\d{3},)?)(\d{1,3})')
            if re.search(finder, line) is not None:
                country_numbers.append(re.search(finder, line).group())
            else:
                country_numbers.append("")
    country_numbers.pop(3)
    return country_numbers
    # # print(country_numbers)
    # country_dict = {"Total Cases": country_numbers[0], "New Cases": country_numbers[1], "Total Deahts": country_numbers[2],
    #                 "New Deaths": country_numbers[4], "Total Recovered": country_numbers[5], "Active Cases": country_numbers[6],
    #                 "Serious, Critical": country_numbers[7], "Total Cases per 1 Million People": country_numbers[8],
    #                 "Deaths per 1 Million People": country_numbers[9], "Total Tests": country_numbers[10],
    #                 "Tests per 1 Million People": country_numbers[11], "Population": country_numbers[12]}

def update_index(country):
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
                          world_numbers[2] + '</span></h3>\n'
            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

    country_numbers = get_country_data(country)
    with open(dir_path, 'r') as f:
        newstr = """"""
        inlines = False
        count = -1
        for line in f.readlines():
            if ('<td class="tg-0pky"><b>' + country) in str(line):
                inlines = True
            if count == 12:
                inlines = False
            if inlines == True:
                newstr += line.replace('x">','x">' + country_numbers[count])
                count += 1
            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()
    print(newstr)
update_index("United States")
# print(get_country_data("United States"))
# print(get_country_data("United States"))
# if __name__ == "__main__":
#     country = str(sys.argv[1])
#     update_date(country)

# mycountries = ['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
# for country in mycountries:
#     update_date(country)
