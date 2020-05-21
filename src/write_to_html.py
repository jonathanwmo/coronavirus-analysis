#!/usr/bin/python3

import datetime
from datetime import datetime, timedelta
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

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
    country_numbers = []

    if country == "world":
        for line in page_list:
            if ('">World') in str(line.strip()):
                inlines = True
            if inlines == True:
                country_numbers_html.append(line)
            if ('data-continent="all"') in str(line):
                break

        country_numbers_html = country_numbers_html[1:]

        for i in range(len(country_numbers_html)):
            myList = [country_numbers_html[i]]
            for line in myList:
                finder = re.compile(r'\b\d[\d,.]*\b')
                if re.search(finder, line) is not None:
                    country_numbers.append(re.search(finder, line).group())
                else:
                    country_numbers.append("")
        country_numbers.pop(5)
        country_numbers.pop(5)
        country_numbers[-1] = '7,785,879,495'

    else:
        for line in page_list:
            if ("country/" + country + "/") in str(line.strip()):
                inlines = True
            if inlines == True:
              country_numbers_html.append(line)
            if ('a href="/world-population/' + country + "-population/") in str(line):
                break

        country_numbers_html = country_numbers_html[1:]

        for i in range(len(country_numbers_html)):
            myList = [country_numbers_html[i]]
            for line in myList:
                finder = re.compile(r'(\d{0,3},)?((\d{3},)?)(\d{1,3})')
                if re.search(finder, line) is not None:
                    country_numbers.append(re.search(finder, line).group())
                else:
                    country_numbers.append("")
        country_numbers.pop(3)
        country_numbers.pop(5)
        country_numbers.pop(5)
    return country_numbers
    # # print(country_numbers)
    # country_dict = {"Total Cases": country_numbers[0], "New Cases": country_numbers[1], "Total Deahts": country_numbers[2],
    #                 "New Deaths": country_numbers[4], "Total Recovered": country_numbers[5], "Active Cases": country_numbers[6],
    #                 "Serious, Critical": country_numbers[7], "Total Cases per 1 Million People": country_numbers[8],
    #                 "Deaths per 1 Million People": country_numbers[9], "Total Tests": country_numbers[10],
    #                 "Tests per 1 Million People": country_numbers[11], "Population": country_numbers[12]}

def update_country_html(country):
    country_numbers = get_country_data(country)
    _country_ = country.lower().replace(" ", "_")
    country = country.lower().replace(" ", "")

    dir_path = os.path.dirname(os.path.realpath(__file__))[0:56] + "/src/htmls/" + country + ".html"

    date_aot = str(datetime.today())[0:10]
    date_aoy = str(datetime.today() - timedelta(days=1))[0:10]
    date_ao2 = str(str(datetime.today() - timedelta(days=2))[0:10])
    date_ao3 = str(str(datetime.today() - timedelta(days=2))[0:10])

    for i in range(len(country_numbers)):
        if country_numbers[i] == "":
            country_numbers[i] = "n/a"
    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            if date_aoy in line:
                newstr += line.replace(date_aoy, date_aot)
            elif date_ao2 in line:
                newstr += line.replace(date_ao2, date_aot)
            elif date_ao3 in line:
                newstr += line.replace(date_ao3, date_aot)
            elif '<p>Total Cases:' in line:
                newstr += '                <p>Total Cases: ' + country_numbers[0] + ' &emsp; &emsp; &emsp; New Cases: ' + country_numbers[1] + ' &emsp; &emsp; &emsp; Total Cases/1 Million Population: ' + country_numbers[5] +'</p>\n'
            elif '<p>Total Deaths' in line:
                newstr += '                <p>Total Deaths: ' + country_numbers[2] + ' &emsp; &emsp; &emsp; New Deaths: ' + country_numbers[3] + ' &emsp; &emsp; &emsp; Deaths/1 Million Population: ' + country_numbers[6] + '</p>\n'
            elif '<p>Total Recovered' in line:
                newstr += '                <p>Total Recovered: ' + country_numbers[4] + ' &emsp; &emsp; &emsp; Total Tests: ' + country_numbers[7] + ' &emsp; &emsp; &emsp; Tests/1 Million Population: ' + country_numbers[8] + '</p>\n'
            elif '<p>Population' in line:
                newstr +='                <p>Population: ' + country_numbers[9] + '</p>\n'

            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

def update_index_html(country):
    titled_country = country.title()
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

    date_aot = str(datetime.today())[0:10]
    dir_path = os.path.dirname(os.path.realpath(__file__))[0:56] + "/index.html"
    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            if "<h3>World Cases:" in line:
                newstr += '					<h3>World Cases: <span style="color: blue;">' + world_numbers[0] + '</span> &emsp; &emsp; &emsp; Deaths: <span style="color: red;">' + world_numbers[1] + '</span> &emsp; &emsp; &emsp; Recovered: <span style="color: rgb(15, 146, 15);">' + world_numbers[2] + '</span></h3>\n'
            elif '<img src="src/graphs/world/world_allfour_' in line:
                newstr += '                    <img src="src/graphs/world/world_allfour_' + date_aot + '.png" width="1100"/> <br><br><br>\n'
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
            if count == 10:
                inlines = False
            if inlines == True:
                if count == -1:
                    newstr += '							<td class="tg-0pky"><b>' + titled_country + '</b></td>\n'
                elif count == 0:
                    newstr += '							<td class="tg-0lax" id="totalcases">' + country_numbers[count] + '</td>' +'\n'
                elif count == 1:
                    newstr += '							<td class="tg-0lax" id="newcases">+' + country_numbers[count] + '</td>' +'\n'
                elif count == 2:
                    newstr += '							<td class="tg-0lax" id="casespermil">' + country_numbers[5] + '</td>' + '\n'
                elif count == 3:
                    newstr += '							<td class="tg-0lax" id="totaldeaths">' + country_numbers[2] + '</td>' +'\n'
                elif count == 4:
                    newstr += '							<td class="tg-0lax" id="newdeaths">+' + country_numbers[3] + '</td>' +'\n'
                elif count == 5:
                    newstr += '							<td class="tg-0lax" id="deathspermil">' + country_numbers[6] + '</td>' +'\n'
                elif count == 6:
                    newstr += '							<td class="tg-0lax" id="totalrecovered">' + country_numbers[4] + '</td>' +'\n'
                elif count == 7:
                    newstr += '							<td class="tg-0lax" id="totaltests">' + country_numbers[count] + '</td>' +'\n'
                elif count == 8:
                    newstr += '							<td class="tg-0lax" id="testspermil">' + country_numbers[count] + '</td>' +'\n'
                elif count == 9:
                    newstr += '							<td class="tg-0lax" id="population">' + country_numbers[count] + '</td>' +'\n'
                else:
                    newstr += '							<td class="tg-0lax">' + country_numbers[count] + '</td>' +'\n'
                count += 1
            else:
                newstr += line
    f.close()

    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

    print(country + str(country_numbers))

# top25 = ["World", "United States", "Russia", "Spain", "Brazil", "United Kingdom", "Italy", "France", "Germany", "Turkey", "Iran", "India", "Peru", "China", "Canada", "Saudi Arabia", "Belgium", "Mexico", "Chile", "Pakistan", "Netherlands", "Qatar", "Ecuador", "Belarus", "Sweden", "Switzerland"]
# for country in top25:
#     update_index_html(country)
    # print(get_country_data(country))
# print(get_country_data("United States"))
# print(get_country_data("United States"))

mycountries = ['World', 'United States', 'United Kingdom', 'Italy', 'Spain', 'France', 'China']
for country in mycountries:
    print(country)
    update_country_html(country)
    print("Finished")

# print(get_country_data("United States"))


# update_country_html("China")