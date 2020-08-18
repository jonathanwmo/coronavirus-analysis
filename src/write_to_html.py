#!/usr/bin/python3

__author__ = "Jonathan Mo"
__credits__ = ["Jonathan Mo"]
__email__ = "jm9hx@virginia.edu"

import datetime
from datetime import datetime, timedelta
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re


def get_country_data(country: str):
    '''
    looks at worldometers.info to get values of Total Cases, New Cases, Total Deaths, New Deaths,
    Total Recovered, Active Cases, Total Cases per 1 Million People, Deaths per 1 Million People,
    Total Tests, Tests per 1 Million People, Population
    Use Beautiful Soup as well as regular expressions to parse html pages
    :param country: string of inputted country
    :return: a list of 10 strings which represent integer values of said values mentioned earlier
    '''
    # handle edge cases and countries that contain more than 1 word, when
    # parsing worldometers.info spaces are replaced by '-'
    country = country.lower().replace(" ", "-")
    if country == "united-states":
        country = "us"
    elif country == "united-kingdom":
        country = "uk"

    req = Request('https://www.worldometers.info/coronavirus/',
                  headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = BeautifulSoup(page, 'html.parser')

    # create a list of each line of the html page
    page_list = str(page).split("\n")

    # country_numbers_html list will contain the desired ~10 lines of html
    # text for given country
    country_numbers_html = []
    # country_numbers list will contain solely the 10 desired values extracted
    # from country_numbers_html using regular expressions
    country_numbers = []

    inlines = False
    if country == "world":  # special case for world data as its formatted differently
        for line in page_list:
            if ('">World') in str(line):
                inlines = True
            # when inlines=True, we are in desired lines of html text for world
            if inlines:
                country_numbers_html.append(line)
            # 'data-continent...' is our list line of desired html text
            if ('data-continent="all"') in str(line):
                break
        # don't need number in first extracted line of html text
        country_numbers_html = country_numbers_html[1:]

        for i in country_numbers_html:
            finder = re.compile(r'\b\d[\d,.]*\b')
            if re.search(finder, i) is not None:
                country_numbers.append(re.search(finder, i).group())
            else:
                # if no match, append an empty string to country_numbers list instead
                country_numbers.append("")
        # won't display 5th and 6th value in my table
        # print("before pop", country_numbers)
        country_numbers.pop(5)
        country_numbers.pop(6)
        country_numbers.pop(5)
        country_numbers[-2] = '7,785,879,495'

    else:
        for line in page_list:
            if ("country/" + country + "/") in str(line.strip()):
                # when inlines=True, we are in desired lines of html text for
                # given country
                inlines = True
            if inlines:
                country_numbers_html.append(line)
            # 'a href....' is our list line of desired html text
            if ('a href="/world-population/' +
                    country + "-population/") in str(line):
                break
        # don't need number in first extracted line of html text
        country_numbers_html = country_numbers_html[1:]

        for i in country_numbers_html:
            finder = re.compile(r'\b\d[\d,.]*\b')
            if re.search(finder, i) is not None:
                country_numbers.append(re.search(finder, i).group())
            else:
                # if no match, append an empty string to country_numbers list
                # instead
                country_numbers.append("")
        # 3rd index is incorrect line spacing on html page so must be taken out
        # of list
        # print("before pop", country_numbers)
        country_numbers.pop(3)
        # won't display 5th and 6th value in my table
        country_numbers.pop(5)
        country_numbers.pop(6)
        country_numbers.pop(5)
    country_numbers = country_numbers[0:10]
    # print("after pop",country_numbers)
    return country_numbers


def update_country_html(country: str):
    '''
    for a given country passed in, this function writes to that country's html page
    to update the data values and which .png image to pull from a given date
    :param country: string of country
    :return: a list of 10 strings which represent integer values
    '''

    # handle edge cases when countries are named differently across different websites
    if country == 'Bonaire Sint Eustatius and Saba':
        country_numbers = get_country_data('caribbean-netherlands')
    elif country == 'Brunei':
        country_numbers = get_country_data('brunei-darussalam')
    elif country == 'Cape Verde':
        country_numbers = get_country_data('cabo-verde')
    elif country == "Cote d'Ivoire":
        country_numbers = get_country_data('cote-d-ivoire')
    elif country == 'Democratic Republic of Congo':
        country_numbers = get_country_data('democratic-republic-of-the-congo')
    elif country == 'Falkland Islands':
        country_numbers = get_country_data('falkland-islands-malvinas')
    elif country == 'Guernsey':
        country_numbers = get_country_data('channel-islands')
    elif country == 'Palestine':
        country_numbers = get_country_data('state-of-palestine')
    elif country == 'Sint Maarten (Dutch part)':
        country_numbers = get_country_data('sint-maarten')
    elif country == 'Timor':
        country_numbers = get_country_data('timor-leste')
    elif country == 'Vatican':
        country_numbers = get_country_data('holy-see')
    elif country == 'Vietnam':
        country_numbers = get_country_data('viet-nam')
    else:
        country_numbers = get_country_data(country)

    _country_ = country.lower().replace(" ", "_")
    country = country.lower().replace(" ", "")

    dir_path = os.path.dirname(os.path.realpath(__file__))[
        0:56] + "/src/htmls/" + country + ".html"

    # create the dates of the past 3 days as strings
    date_aot = str(datetime.today())[0:10]
    date_aoy = str(datetime.today() - timedelta(days=1))[0:10]
    date_ao2 = str(str(datetime.today() - timedelta(days=2))[0:10])
    date_ao3 = str(str(datetime.today() - timedelta(days=3))[0:10])
    date_ao4 = str(str(datetime.today() - timedelta(days=4))[0:10])
    date_ao5 = str(str(datetime.today() - timedelta(days=5))[0:10])
    date_ao6 = str(str(datetime.today() - timedelta(days=6))[0:10])




    # replace any empty values with n/a
    for i in range(len(country_numbers)):
        if country_numbers[i] == "":
            country_numbers[i] = "n/a"

    # open country html file for reading
    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            # update the dates
            if date_aoy in line:
                newstr += line.replace(date_aoy, date_aot)
            elif date_ao2 in line:
                newstr += line.replace(date_ao2, date_aot)
            elif date_ao3 in line:
                newstr += line.replace(date_ao3, date_aot)
            elif date_ao4 in line:
                newstr += line.replace(date_ao4, date_aot)
            elif date_ao5 in line:
                newstr += line.replace(date_ao5, date_aot)
            elif date_ao6 in line:
                newstr += line.replace(date_ao6, date_aot)
            # update the values on html page as scraped from worldometer.info
            # site
            elif '<li class="nav-item"><input type="type" placeholder="Search for a country..." name="search" id="search"> </form> </li>' in line:
                newstr += '                <li><input id="searchbar" onkeyup="search_country()" type="type" placeholder="Search for a country..." name="search" id="searchbar"> </form> </li>\n'

            elif '<p><b><u>Total Cases</u></b><br><br> ' in line:
                newstr += '                    <p><b><u>Total Cases</u></b><br><br> ' + \
                    country_numbers[0] + '</p>\n'
            elif '<p><b><u>New Cases </u></b><br><br>' in line:
                newstr += '                    <p><b><u>New Cases </u></b><br><br>' + \
                    country_numbers[1] + '</p>\n'
            elif '<p><b><u>Cases/1 Million </u></b><b' in line:
                newstr += '                    <p><b><u>Cases/1 Million </u></b><br><br>' + \
                    country_numbers[5] + '</p>\n'
            elif '<p><b><u>Total Deaths </u></b><br><' in line:
                newstr += '                    <p><b><u>Total Deaths </u></b><br><br>' + \
                    country_numbers[2] + '</p>\n'
            elif '<p><b><u>New Deaths </u></b><br><br' in line:
                newstr += '                    <p><b><u>New Deaths </u></b><br><br>' + \
                    country_numbers[3] + '</p>\n'
            elif '<p><b><u>Deaths/1 Million</u></b><b' in line:
                newstr += '                    <p><b><u>Deaths/1 Million</u></b><br><br>' + \
                    country_numbers[6] + '</p>\n'
            elif '<p><b><u>Total Recovered </u></b><b' in line:
                newstr += '                    <p><b><u>Total Recovered </u></b><br><br>' + \
                    country_numbers[4] + '</p>\n'
            elif '<p><b><u>Total Tests </u></b><br><b' in line:
                newstr += '                    <p><b><u>Total Tests </u></b><br><br>' + \
                    country_numbers[7] + '</p>\n'
            elif '<p><b><u>Tests/1 Million</u></b><br' in line:
                newstr += '                    <p><b><u>Tests/1 Million</u></b><br><br>' + \
                    country_numbers[8] + '</p>\n'
            elif '<p><b><u>Population</u></b><br><br>' in line:
                newstr += '                    <p><b><u>Population</u></b><br><br>' + \
                    country_numbers[9] + '</p>\n'
            else:
                newstr += line
    f.close()

    # update html file by writing data to file
    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

    return country_numbers


def update_index_html(country: str):
    '''
    updates the graph on main index page as well as the data in the table of the top 25 most affect countries
    :param country: country to be updated in the table on the home index page
    :return: void
    '''
    titled_country = country.title()
    req = Request('https://www.worldometers.info/coronavirus/',
                  headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = BeautifulSoup(page, 'html.parser')

    # get a list of the main numbers using html 'class="maincounter-number"'
    # separator
    world_numbers_html = page.findAll("div", class_="maincounter-number")
    world_numbers = []

    for number in world_numbers_html:
        # use regex to extract numbers from world_numbers_html, put those
        # numbers in world_numbers list
        finder = re.compile(r'\b\d[\d,.]*\b')
        for match in finder.finditer(str(number)):
            world_numbers.append(match.group())

    date_aot = str(datetime.today())[0:10]
    dir_path = os.path.dirname(
        os.path.realpath(__file__))[:-4] + "/index.html"
    with open(dir_path, 'r') as f:
        newstr = """"""
        for line in f.readlines():
            # update main info for world
            if "<h3>World Cases:" in line:
                newstr += '					<h3>World Cases: <span style="color: blue;">' + world_numbers[0] + \
                          '</span> &emsp; &emsp; &emsp; Deaths: <span style="color: red;">' + \
                    world_numbers[1] + \
                          '</span> &emsp; &emsp; &emsp; Recovered: <span style="color: rgb(15, 146, 15);">' + \
                          world_numbers[2] + '</span></h3>\n'
            # update date for pulling graph .png file
            elif '<img src="src/graphs/world/world_allfour_' in line:
                newstr += '                    <img src="src/graphs/world/world_allfour_' + \
                    date_aot + '.png" width="1100"/> <br><br><br>\n'
            else:
                newstr += line
    f.close()
    # update html page by writing data to file
    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

    # update data in table on main index.html page
    country_numbers = get_country_data(country)
    country_lower = country.lower().replace(" ", "")
    with open(dir_path, 'r') as f:
        newstr = """"""
        inlines = False
        count = -1
        for line in f.readlines():
            if ('<td class="tg-0pky" id="country"><b><a href="src/htmls/' + country_lower) in str(line) or ('<td class="tg-0pky"><b>' + titled_country in str(line)):
                inlines = True
            if count == 10:
                inlines = False
            # when in desired lines, update value depending on given category
            if inlines:
                if count == -1:
                    newstr += '							<td class="tg-0pky" id="country"><b><a href="src/htmls/' + \
                              country_lower + '.html">' + titled_country + '</a></b></td>\n'
                elif count == 0:
                    newstr += '							<td class="tg-0lax" id="totalcases">' + \
                        country_numbers[count] + '</td>' + '\n'
                elif count == 1:
                    newstr += '							<td class="tg-0lax" id="newcases">+' + \
                        country_numbers[count] + '</td>' + '\n'
                elif count == 2:
                    newstr += '							<td class="tg-0lax" id="casespermil">' + \
                        country_numbers[5] + '</td>' + '\n'
                elif count == 3:
                    newstr += '							<td class="tg-0lax" id="totaldeaths">' + \
                        country_numbers[2] + '</td>' + '\n'
                elif count == 4:
                    newstr += '							<td class="tg-0lax" id="newdeaths">+' + \
                        country_numbers[3] + '</td>' + '\n'
                elif count == 5:
                    newstr += '							<td class="tg-0lax" id="deathspermil">' + \
                        country_numbers[6] + '</td>' + '\n'
                elif count == 6:
                    newstr += '							<td class="tg-0lax" id="totalrecovered">' + \
                        country_numbers[4] + '</td>' + '\n'
                elif count == 7:
                    newstr += '							<td class="tg-0lax" id="totaltests">' + \
                        country_numbers[count] + '</td>' + '\n'
                elif count == 8:
                    newstr += '							<td class="tg-0lax" id="testspermil">' + \
                        country_numbers[count] + '</td>' + '\n'
                elif count == 9:
                    newstr += '							<td class="tg-0lax" id="population">' + \
                        country_numbers[count] + '</td>' + '\n'
                else:
                    newstr += '							<td class="tg-0lax">' + \
                        country_numbers[count] + '</td>' + '\n'
                count += 1
            else:
                newstr += line
    f.close()
    # update html page page by writing to file
    with open(dir_path, 'w') as f:
        f.write(newstr)
    f.close()

    print(country + str(country_numbers))

top25 = [
    "World",
    "United States",
    "Russia",
    "Spain",
    "Brazil",
    "United Kingdom",
    "Italy",
    "France",
    "Germany",
    "Turkey",
    "Iran",
    "India",
    "Peru",
    "China",
    "Canada",
    "Saudi Arabia",
    "Belgium",
    "Mexico",
    "Chile",
    "Pakistan",
    "Netherlands",
    "Qatar",
    "Ecuador",
    "Belarus",
    "Sweden",
    "Singapore"]
for country in top25:
    update_index_html(country)

all_countries = [
    'World',
    'Afghanistan',
    'Albania',
    'Algeria',
    'Andorra',
    'Angola',
    'Anguilla',
    'Antigua and Barbuda',
    'Argentina',
    'Armenia',
    'Aruba',
    'Australia',
    'Austria',
    'Azerbaijan',
    'Bahamas',
    'Bahrain',
    'Bangladesh',
    'Barbados',
    'Belarus',
    'Belgium',
    'Belize',
    'Benin',
    'Bermuda',
    'Bhutan',
    'Bolivia',
    'Bonaire Sint Eustatius and Saba',
    'Bosnia and Herzegovina',
    'Botswana',
    'Brazil',
    'British Virgin Islands',
    'Brunei',
    'Bulgaria',
    'Burkina Faso',
    'Burundi',
    'Cambodia',
    'Cameroon',
    'Canada',
    'Cape Verde',
    'Cayman Islands',
    'Central African Republic',
    'Chad',
    'Chile',
    'China',
    'Colombia',
    'Comoros',
    'Congo',
    'Costa Rica',
    "Cote d'Ivoire",
    'Croatia',
    'Cuba',
    'Curacao',
    'Cyprus',
    'Czech Republic',
    'Democratic Republic of Congo',
    'Denmark',
    'Djibouti',
    'Dominica',
    'Dominican Republic',
    'Ecuador',
    'Egypt',
    'El Salvador',
    'Equatorial Guinea',
    'Eritrea',
    'Estonia',
    'Ethiopia',
    'Faeroe Islands',
    'Falkland Islands',
    'Fiji',
    'Finland',
    'France',
    'French Polynesia',
    'Gabon',
    'Gambia',
    'Georgia',
    'Germany',
    'Ghana',
    'Gibraltar',
    'Greece',
    'Greenland',
    'Grenada',
    'Guam',
    'Guatemala',
    'Guernsey',
    'Guinea',
    'Guinea-Bissau',
    'Guyana',
    'Haiti',
    'Honduras',
    'Hungary',
    'Iceland',
    'India',
    'Indonesia',
    'Iran',
    'Iraq',
    'Ireland',
    'Isle of Man',
    'Israel',
    'Italy',
    'Jamaica',
    'Japan',
    'Jersey',
    'Jordan',
    'Kazakhstan',
    'Kenya',
    'Kosovo',
    'Kuwait',
    'Kyrgyzstan',
    'Laos',
    'Latvia',
    'Lebanon',
    'Liberia',
    'Libya',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Macedonia',
    'Madagascar',
    'Malawi',
    'Malaysia',
    'Maldives',
    'Mali',
    'Malta',
    'Mauritania',
    'Mauritius',
    'Mexico',
    'Moldova',
    'Monaco',
    'Mongolia',
    'Montenegro',
    'Montserrat',
    'Morocco',
    'Mozambique',
    'Myanmar',
    'Namibia',
    'Nepal',
    'Netherlands',
    'New Caledonia',
    'New Zealand',
    'Nicaragua',
    'Niger',
    'Nigeria',
    'Northern Mariana Islands',
    'Norway',
    'Oman',
    'Pakistan',
    'Palestine',
    'Panama',
    'Papua New Guinea',
    'Paraguay',
    'Peru',
    'Philippines',
    'Poland',
    'Portugal',
    'Puerto Rico',
    'Qatar',
    'Romania',
    'Russia',
    'Rwanda',
    'Saint Kitts and Nevis',
    'Saint Lucia',
    'Saint Vincent and the Grenadines',
    'San Marino',
    'Sao Tome and Principe',
    'Saudi Arabia',
    'Senegal',
    'Serbia',
    'Seychelles',
    'Sierra Leone',
    'Singapore',
    'Sint Maarten (Dutch part)',
    'Slovakia',
    'Slovenia',
    'Somalia',
    'South Africa',
    'South Korea',
    'South Sudan',
    'Spain',
    'Sri Lanka',
    'Sudan',
    'Suriname',
    'Swaziland',
    'Sweden',
    'Switzerland',
    'Syria',
    'Taiwan',
    'Tajikistan',
    'Tanzania',
    'Thailand',
    'Timor',
    'Togo',
    'Trinidad and Tobago',
    'Tunisia',
    'Turkey',
    'Turks and Caicos Islands',
    'Uganda',
    'Ukraine',
    'United Arab Emirates',
    'United Kingdom',
    'United States',
    'United States Virgin Islands',
    'Uruguay',
    'Uzbekistan',
    'Vatican',
    'Venezuela',
    'Vietnam',
    'Western Sahara',
    'Yemen',
    'Zambia',
    'Zimbabwe']

for country in all_countries:
    if country == "Guam" or country == "International" or country == "Jersey" or country == "Kosovo" or \
            country == "Northern Mariana Islands" or country == "Puerto Rico" or \
            country == "United States Virgin Islands":
        pass
    else:
        index = all_countries.index(country) + 1
        print(country + ": " + str(index) + "/" +
              str(len(all_countries)), update_country_html(country))
        print("Finished")
